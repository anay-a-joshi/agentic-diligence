"""Generates the LBO Excel workbook (5-year proj + sensitivity + returns)."""
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def _hdr_fill(): return PatternFill("solid", fgColor="0A2540")
def _row_alt(): return PatternFill("solid", fgColor="F5F7FA")
def _bull_fill(): return PatternFill("solid", fgColor="DCFCE7")
def _base_fill(): return PatternFill("solid", fgColor="FEF3C7")
def _bear_fill(): return PatternFill("solid", fgColor="FEE2E2")
def _white_bold(): return Font(bold=True, color="FFFFFF")
def _bold(): return Font(bold=True)
def _border():
    s = Side(style="thin", color="CBD5E1")
    return Border(left=s, right=s, top=s, bottom=s)


def _write_scenario_sheet(ws, scenario_name: str, scenario: dict, fill: PatternFill):
    """Write one scenario's full projection."""
    ws.merge_cells("A1:G1")
    ws["A1"] = f"{scenario_name.upper()} CASE"
    ws["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws["A1"].fill = _hdr_fill()
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26

    # Inputs
    ws["A3"] = "Inputs"
    ws["A3"].font = _bold()
    inputs = scenario.get("inputs", {})
    input_rows = [
        ("Purchase Price ($M)", inputs.get("purchase_price_usd_millions")),
        ("Debt at Close ($M)", inputs.get("debt_at_close_usd_millions")),
        ("Sponsor Equity at Close ($M)", inputs.get("sponsor_equity_at_close_usd_millions")),
        ("Revenue Growth Assumption (%)", inputs.get("revenue_growth_pct")),
        ("EBITDA Margin Y5 (%)", inputs.get("ebitda_margin_y5_pct")),
        ("Exit Multiple (EV/EBITDA)", inputs.get("exit_multiple")),
        ("Leverage at Close (%)", inputs.get("debt_pct")),
        ("Hold Period (years)", inputs.get("hold_period_years")),
    ]
    for i, (k, v) in enumerate(input_rows, start=4):
        ws.cell(row=i, column=1, value=k)
        ws.cell(row=i, column=2, value=v)

    # Projections table
    proj = scenario.get("projections", {})
    years = proj.get("year", [])
    start_row = 14
    headers = ["Metric ($M)"] + [f"Year {y}" for y in years]
    for ci, h in enumerate(headers, start=1):
        c = ws.cell(row=start_row, column=ci, value=h)
        c.font = _white_bold()
        c.fill = _hdr_fill()
        c.alignment = Alignment(horizontal="center")
        c.border = _border()

    rows = [
        ("Revenue", proj.get("revenue_usd_millions", [])),
        ("EBITDA", proj.get("ebitda_usd_millions", [])),
        ("Free Cash Flow", proj.get("fcf_usd_millions", [])),
        ("Debt Balance (EoY)", proj.get("debt_balance_usd_millions", [])),
    ]
    for ri, (label, values) in enumerate(rows, start=start_row + 1):
        c = ws.cell(row=ri, column=1, value=label)
        c.font = _bold()
        c.border = _border()
        for ci, val in enumerate(values, start=2):
            cc = ws.cell(row=ri, column=ci, value=val)
            cc.number_format = "#,##0"
            cc.border = _border()
            if ri % 2 == 0:
                cc.fill = _row_alt()

    # Exit & Returns
    exit_row = start_row + len(rows) + 3
    ws.cell(row=exit_row, column=1, value="Exit & Returns").font = _bold()
    exit_data = scenario.get("exit", {})
    returns = scenario.get("returns", {})
    summary = [
        ("Exit EBITDA ($M)", exit_data.get("exit_ebitda_usd_millions")),
        ("Exit EV ($M)", exit_data.get("exit_ev_usd_millions")),
        ("Remaining Debt ($M)", exit_data.get("remaining_debt_usd_millions")),
        ("Exit Equity Value ($M)", exit_data.get("exit_equity_value_usd_millions")),
        ("MOIC", returns.get("moic")),
        ("IRR (%)", returns.get("irr_pct")),
    ]
    for i, (k, v) in enumerate(summary, start=exit_row + 1):
        c1 = ws.cell(row=i, column=1, value=k)
        c2 = ws.cell(row=i, column=2, value=v)
        c1.fill = fill
        c2.fill = fill
        if "MOIC" in k:
            c2.number_format = "0.00\"x\""
            c2.font = Font(bold=True, color="0A2540")
        elif "IRR" in k:
            c2.number_format = "0.0\"%\""
            c2.font = Font(bold=True, color="0A2540")
        else:
            c2.number_format = "#,##0"

    # Column widths
    ws.column_dimensions["A"].width = 32
    for col in range(2, 9):
        ws.column_dimensions[get_column_letter(col)].width = 14


def _write_sensitivity_sheet(ws, base_scenario: dict):
    """Sensitivity: IRR as function of Exit Multiple × Revenue Growth."""
    ws.merge_cells("A1:H1")
    ws["A1"] = "SENSITIVITY: BASE-CASE IRR (% by Exit Multiple × Revenue Growth)"
    ws["A1"].font = Font(bold=True, size=12, color="FFFFFF")
    ws["A1"].fill = _hdr_fill()
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    # Pull base inputs needed for re-running mini-scenarios
    inputs = base_scenario.get("inputs", {})
    # Show a 5x5 table — exit multiples 10x..14x, growth 1%..7%
    exit_mults = [10.0, 11.0, 12.0, 13.0, 14.0]
    growths = [1.0, 3.0, 4.0, 5.0, 7.0]

    # Top header row
    ws.cell(row=3, column=1, value="").fill = _hdr_fill()
    for ci, m in enumerate(exit_mults, start=2):
        c = ws.cell(row=3, column=ci, value=f"{m:.1f}x")
        c.font = _white_bold()
        c.fill = _hdr_fill()
        c.alignment = Alignment(horizontal="center")
        c.border = _border()

    # Compute IRRs row-by-row
    from app.services.lbo_engine import run_lbo_scenario

    for ri, growth in enumerate(growths, start=4):
        c = ws.cell(row=ri, column=1, value=f"Growth {growth:.1f}%")
        c.font = _bold()
        c.fill = _hdr_fill()
        c.font = _white_bold()
        c.border = _border()

        for ci, m in enumerate(exit_mults, start=2):
            try:
                # Reconstruct minimal scenario inputs from base
                rev_y0 = base_scenario["projections"]["revenue_usd_millions"][0] / (1 + inputs["revenue_growth_pct"] / 100)
                ebitda_y0 = base_scenario["projections"]["ebitda_usd_millions"][0]
                # Approximate margin from y0 EBITDA / y0 revenue
                margin_y0_pct = (ebitda_y0 / rev_y0 * 100.0) if rev_y0 > 0 else 30.0

                # Re-run scenario with new growth & exit multiple
                # We approximate by reusing the purchase-price + sponsor-equity from base
                tp_total = (inputs["purchase_price_usd_millions"] +
                            (base_scenario.get("inputs", {}).get("debt_at_close_usd_millions", 0) * 0))  # purchase already includes both
                # Simpler: we reuse the purchase math directly via debt+equity
                debt = inputs["debt_at_close_usd_millions"]
                eq = inputs["sponsor_equity_at_close_usd_millions"]
                tp_total = debt + eq

                result = run_lbo_scenario(
                    ebitda_y0=ebitda_y0,
                    revenue_y0=rev_y0,
                    take_private_price_total=tp_total,
                    cash_on_balance_sheet=0,  # already netted
                    existing_debt=0,
                    revenue_growth_pct=growth,
                    ebitda_margin_y5_pct=margin_y0_pct + 1.0,
                    exit_multiple=m,
                    debt_pct_of_purchase=eq / (debt + eq) if (debt + eq) > 0 else 0.55,
                )
                irr = result["returns"]["irr_pct"]
            except Exception:
                irr = None
            cc = ws.cell(row=ri, column=ci, value=irr)
            cc.number_format = "0.0\"%\""
            cc.alignment = Alignment(horizontal="center")
            cc.border = _border()

            # Heat-map color coding
            if isinstance(irr, (int, float)):
                if irr >= 25: cc.fill = PatternFill("solid", fgColor="86EFAC")
                elif irr >= 20: cc.fill = PatternFill("solid", fgColor="BBF7D0")
                elif irr >= 15: cc.fill = PatternFill("solid", fgColor="FEF3C7")
                elif irr >= 10: cc.fill = PatternFill("solid", fgColor="FED7AA")
                else: cc.fill = PatternFill("solid", fgColor="FECACA")

    ws.column_dimensions["A"].width = 18
    for col in range(2, 7):
        ws.column_dimensions[get_column_letter(col)].width = 12


def generate_lbo_excel(
    ticker: str,
    company_name: str,
    output_dir: str,
    lbo: dict,
    financial: dict,
    market: dict,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{ticker}_LBO_Model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(output_dir, filename)

    wb = Workbook()
    wb.remove(wb.active)

    # Summary tab
    ws_sum = wb.create_sheet("Summary")
    ws_sum.merge_cells("A1:E1")
    ws_sum["A1"] = f"{ticker} — {company_name}: LBO Returns Summary"
    ws_sum["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws_sum["A1"].fill = _hdr_fill()
    ws_sum["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_sum.row_dimensions[1].height = 28

    headers = ["Scenario", "IRR (%)", "MOIC", "Exit Equity ($M)", "Exit EV ($M)"]
    for ci, h in enumerate(headers, start=1):
        c = ws_sum.cell(row=3, column=ci, value=h)
        c.font = _white_bold()
        c.fill = _hdr_fill()
        c.border = _border()
        c.alignment = Alignment(horizontal="center")

    if lbo.get("status") == "ok":
        rows = [
            ("Base", lbo["base"], _base_fill()),
            ("Bull", lbo["bull"], _bull_fill()),
            ("Bear", lbo["bear"], _bear_fill()),
        ]
        for i, (name, sc, fill) in enumerate(rows, start=4):
            ws_sum.cell(row=i, column=1, value=name).fill = fill
            ws_sum.cell(row=i, column=2, value=sc["returns"]["irr_pct"]).fill = fill
            ws_sum.cell(row=i, column=3, value=sc["returns"]["moic"]).fill = fill
            ws_sum.cell(row=i, column=4, value=sc["exit"]["exit_equity_value_usd_millions"]).fill = fill
            ws_sum.cell(row=i, column=5, value=sc["exit"]["exit_ev_usd_millions"]).fill = fill
            ws_sum.cell(row=i, column=2).number_format = "0.0\"%\""
            ws_sum.cell(row=i, column=3).number_format = "0.00\"x\""
            ws_sum.cell(row=i, column=4).number_format = "#,##0"
            ws_sum.cell(row=i, column=5).number_format = "#,##0"
            for col in range(1, 6):
                ws_sum.cell(row=i, column=col).border = _border()

    for col in range(1, 6):
        ws_sum.column_dimensions[get_column_letter(col)].width = 18

    # Per-scenario tabs
    if lbo.get("status") == "ok":
        ws_base = wb.create_sheet("Base Case")
        _write_scenario_sheet(ws_base, "Base", lbo["base"], _base_fill())

        ws_bull = wb.create_sheet("Bull Case")
        _write_scenario_sheet(ws_bull, "Bull", lbo["bull"], _bull_fill())

        ws_bear = wb.create_sheet("Bear Case")
        _write_scenario_sheet(ws_bear, "Bear", lbo["bear"], _bear_fill())

        ws_sens = wb.create_sheet("Sensitivity")
        _write_sensitivity_sheet(ws_sens, lbo["base"])

    # Inputs reference tab
    ws_inputs = wb.create_sheet("Inputs Reference")
    ws_inputs["A1"] = "Inputs from Diligence Pipeline"
    ws_inputs["A1"].font = _bold()
    refs = [
        ("Ticker", ticker),
        ("Company", company_name),
        ("Revenue ($M)", financial.get("revenue_usd_millions")),
        ("EBITDA ($M)", financial.get("ebitda_usd_millions")),
        ("EBITDA Margin (%)", financial.get("ebitda_margin_pct")),
        ("Free Cash Flow ($M)", financial.get("free_cash_flow_usd_millions")),
        ("Total Debt ($M)", financial.get("total_debt_usd_millions")),
        ("Cash ($M)", financial.get("cash_and_equivalents_usd_millions")),
        ("Market Cap ($M)", market.get("market_cap_usd_millions")),
        ("Current Price", market.get("current_price")),
        ("P/E", market.get("pe_ratio")),
        ("EV/EBITDA", market.get("ev_to_ebitda")),
        ("Beta", market.get("beta")),
    ]
    for i, (k, v) in enumerate(refs, start=3):
        ws_inputs.cell(row=i, column=1, value=k).font = _bold()
        ws_inputs.cell(row=i, column=2, value=v)
    ws_inputs.column_dimensions["A"].width = 28
    ws_inputs.column_dimensions["B"].width = 22

    wb.save(filepath)
    return filepath
