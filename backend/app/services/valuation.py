"""DCF + comparable company analysis (CCA)."""


def run_dcf(
    fcf_projections: list[float],
    terminal_growth: float,
    wacc: float,
) -> float:
    """Discount projected FCFs + terminal value back to PV."""
    pv = 0.0
    for t, fcf in enumerate(fcf_projections, start=1):
        pv += fcf / ((1 + wacc) ** t)
    terminal_value = fcf_projections[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv += terminal_value / ((1 + wacc) ** len(fcf_projections))
    return pv


def run_cca(target_ebitda: float, peer_multiples: list[float]) -> dict:
    """Apply peer median/mean multiples to target EBITDA."""
    import statistics
    return {
        "median_ev": target_ebitda * statistics.median(peer_multiples),
        "mean_ev": target_ebitda * statistics.mean(peer_multiples),
        "min_ev": target_ebitda * min(peer_multiples),
        "max_ev": target_ebitda * max(peer_multiples),
    }
