"""Composite Take-Private Feasibility Score (0-100)."""


def compute_feasibility_score(
    valuation_gap: float,      # IRR vs hurdle
    governance_score: float,   # 0-1, friendlier = higher
    financial_score: float,    # 0-1, FCF stability
    leverage_capacity: float,  # 0-1
) -> int:
    """
    Weighted composite. Tweak weights as the model matures.
    """
    weights = {"val": 0.4, "gov": 0.2, "fin": 0.25, "lev": 0.15}
    raw = (
        weights["val"] * min(max(valuation_gap, 0), 1)
        + weights["gov"] * governance_score
        + weights["fin"] * financial_score
        + weights["lev"] * leverage_capacity
    )
    return int(round(raw * 100))
