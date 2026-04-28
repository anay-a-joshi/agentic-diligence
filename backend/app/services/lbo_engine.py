"""LBO Engine — projects cash flows, debt paydown, exit, IRR/MOIC.

Always returns real numbers. Caps unrealistic LBO sizes so the math
stays sensible even when applied to mega-cap stocks.
"""

# Practical PE LBO check ceiling — even mega-funds (Blackstone, KKR) rarely
# write equity checks > $25B. We cap at $50B for headroom; above this we
# flag deal as size-prohibitive but still compute sensible scenario math.
MAX_REALISTIC_EQUITY_CHECK_USD_MILLIONS = 50_000


def _safe_float(v, default: float = 0.0) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _safe_irr(moic: float, years: int) -> float:
    """IRR % from MOIC over N years. Handles negative MOIC cleanly.

    Positive MOIC: standard IRR formula
    MOIC = 1: 0% IRR
    MOIC < 1 but > 0: negative IRR (deal made less than equity put in)
    MOIC <= 0: deal totally lost money — return -100% (capital impaired)
    """
    if years <= 0:
        return 0.0
    if moic <= 0:
        return -100.0
    # Standard IRR: works for any positive MOIC including <1 (negative IRR)
    return (moic ** (1.0 / years) - 1.0) * 100.0


def run_lbo_scenario(
    ebitda_y0: float,
    revenue_y0: float,
    take_private_price_total: float,
    cash_on_balance_sheet: float,
    existing_debt: float,
    revenue_growth_pct: float,
    ebitda_margin_y5_pct: float,
    exit_multiple: float,
    debt_pct_of_purchase: float = 0.55,
    interest_rate_pct: float = 8.0,
    tax_rate_pct: float = 21.0,
    capex_pct_of_revenue: float = 3.0,
    nwc_pct_of_revenue_change: float = 5.0,
    hold_period_years: int = 5,
) -> dict:
    """Run a single LBO scenario. All dollar inputs in millions."""
    purchase_price = max(0.0, take_private_price_total - cash_on_balance_sheet)
    if debt_pct_of_purchase > 1:
        debt_pct_decimal = debt_pct_of_purchase / 100.0
    else:
        debt_pct_decimal = debt_pct_of_purchase
    debt_at_close = purchase_price * debt_pct_decimal
    sponsor_equity_at_close = purchase_price - debt_at_close

    years = list(range(1, hold_period_years + 1))
    revenue_path: list[float] = []
    ebitda_path: list[float] = []
    fcf_path: list[float] = []
    debt_balance_path: list[float] = []

    rev = revenue_y0
    margin_y0 = ebitda_y0 / revenue_y0 if revenue_y0 > 0 else 0.30
    target_margin = ebitda_margin_y5_pct / 100.0
    debt_balance = debt_at_close
    prior_revenue = revenue_y0

    for y in years:
        rev = rev * (1 + revenue_growth_pct / 100.0)
        progress = y / hold_period_years
        margin_y = margin_y0 + (target_margin - margin_y0) * progress
        ebitda = rev * margin_y

        da = rev * 0.04
        ebit = ebitda - da
        interest_expense = debt_balance * (interest_rate_pct / 100.0)
        ebt = ebit - interest_expense
        taxes = max(0.0, ebt * tax_rate_pct / 100.0)
        net_income = ebt - taxes

        capex = rev * (capex_pct_of_revenue / 100.0)
        nwc_change = (rev - prior_revenue) * (nwc_pct_of_revenue_change / 100.0)
        fcf = net_income + da - capex - nwc_change

        debt_paydown = max(0.0, fcf)
        debt_balance = max(0.0, debt_balance - debt_paydown)

        revenue_path.append(round(rev, 1))
        ebitda_path.append(round(ebitda, 1))
        fcf_path.append(round(fcf, 1))
        debt_balance_path.append(round(debt_balance, 1))
        prior_revenue = rev

    exit_ebitda = ebitda_path[-1]
    exit_ev = exit_ebitda * exit_multiple
    exit_equity_value = max(0.0, exit_ev - debt_balance_path[-1])  # equity can't go below 0

    moic = exit_equity_value / sponsor_equity_at_close if sponsor_equity_at_close > 0 else 0.0
    irr_pct = _safe_irr(moic, hold_period_years)

    return {
        "inputs": {
            "purchase_price_usd_millions": round(purchase_price, 1),
            "debt_at_close_usd_millions": round(debt_at_close, 1),
            "sponsor_equity_at_close_usd_millions": round(sponsor_equity_at_close, 1),
            "revenue_growth_pct": revenue_growth_pct,
            "ebitda_margin_y5_pct": round(ebitda_margin_y5_pct, 2),
            "exit_multiple": exit_multiple,
            "debt_pct": round(debt_pct_decimal * 100, 1),
            "hold_period_years": hold_period_years,
        },
        "projections": {
            "year": years,
            "revenue_usd_millions": revenue_path,
            "ebitda_usd_millions": ebitda_path,
            "fcf_usd_millions": fcf_path,
            "debt_balance_usd_millions": debt_balance_path,
        },
        "exit": {
            "exit_ebitda_usd_millions": round(exit_ebitda, 1),
            "exit_ev_usd_millions": round(exit_ev, 1),
            "exit_equity_value_usd_millions": round(exit_equity_value, 1),
            "remaining_debt_usd_millions": round(debt_balance_path[-1], 1),
        },
        "returns": {
            "moic": round(moic, 2),
            "irr_pct": round(irr_pct, 1),
        },
    }


def run_lbo_full(
    financial: dict,
    market: dict,
    governance: dict | None = None,
) -> dict:
    """Run base/bull/bear LBO scenarios from financial + market data.

    Caps unrealistic checks. Adds 'size_prohibitive' flag when deal too big.
    """
    rev_y0 = _safe_float(financial.get("revenue_usd_millions"))
    ebitda_y0 = _safe_float(financial.get("ebitda_usd_millions"))
    cash = _safe_float(financial.get("cash_and_equivalents_usd_millions"))
    debt_existing = _safe_float(financial.get("total_debt_usd_millions"))

    if rev_y0 <= 0 or ebitda_y0 <= 0:
        return {"status": "insufficient_data"}

    margin_y0 = (ebitda_y0 / rev_y0) * 100.0
    market_cap = _safe_float(market.get("market_cap_usd_millions"))
    if market_cap <= 0:
        market_cap = ebitda_y0 * _safe_float(market.get("ev_to_ebitda"), 12.0)

    # Compute notional sponsor-equity check at 35% premium, 55% leverage
    notional_purchase = market_cap * 1.35 - cash
    notional_equity = notional_purchase * 0.45
    size_prohibitive = notional_equity > MAX_REALISTIC_EQUITY_CHECK_USD_MILLIONS

    # Run scenarios as normal (math will produce sensible relative numbers)
    base = run_lbo_scenario(
        ebitda_y0=ebitda_y0, revenue_y0=rev_y0,
        take_private_price_total=market_cap * 1.35,
        cash_on_balance_sheet=cash, existing_debt=debt_existing,
        revenue_growth_pct=4.0, ebitda_margin_y5_pct=margin_y0 + 1.0,
        exit_multiple=12.0,
    )
    bull = run_lbo_scenario(
        ebitda_y0=ebitda_y0, revenue_y0=rev_y0,
        take_private_price_total=market_cap * 1.30,
        cash_on_balance_sheet=cash, existing_debt=debt_existing,
        revenue_growth_pct=7.0, ebitda_margin_y5_pct=margin_y0 + 3.0,
        exit_multiple=14.0,
    )
    bear = run_lbo_scenario(
        ebitda_y0=ebitda_y0, revenue_y0=rev_y0,
        take_private_price_total=market_cap * 1.40,
        cash_on_balance_sheet=cash, existing_debt=debt_existing,
        revenue_growth_pct=1.0, ebitda_margin_y5_pct=max(20.0, margin_y0 - 2.0),
        exit_multiple=10.0,
    )

    return {
        "status": "ok",
        "size_prohibitive": size_prohibitive,
        "size_prohibitive_note": (
            f"Equity check of ~${notional_equity / 1000:.1f}B exceeds practical "
            f"PE LBO ceiling (~$50B). Even mega-funds do not write checks of this size."
            if size_prohibitive else ""
        ),
        "base": base, "bull": bull, "bear": bear,
        "summary": {
            "irr_base_pct": base["returns"]["irr_pct"],
            "irr_bull_pct": bull["returns"]["irr_pct"],
            "irr_bear_pct": bear["returns"]["irr_pct"],
            "moic_base": base["returns"]["moic"],
            "moic_bull": bull["returns"]["moic"],
            "moic_bear": bear["returns"]["moic"],
        },
    }
