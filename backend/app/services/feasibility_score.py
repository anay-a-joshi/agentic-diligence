"""Take-Private Feasibility Score (0-100) with category breakdown.

Composite of 6 dimensions, each scored 0-100, then weighted-averaged.
"""
from typing import Any


def _safe_get(d: Any, key: str, default=None):
    if not isinstance(d, dict):
        return default
    return d.get(key, default)


def _safe_float(v, default: float = 0.0) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def score_financial_quality(financial: dict | None) -> tuple[int, str]:
    """Higher EBITDA margin & FCF conversion → better. Out of 100."""
    if not financial:
        return 50, "Insufficient financial data"

    ebitda_margin = _safe_float(financial.get("ebitda_margin_pct"))
    revenue = _safe_float(financial.get("revenue_usd_millions"))
    fcf = _safe_float(financial.get("free_cash_flow_usd_millions"))
    yoy_growth = _safe_float(financial.get("revenue_growth_yoy_pct"))

    score = 50.0
    if ebitda_margin >= 30: score += 25
    elif ebitda_margin >= 20: score += 15
    elif ebitda_margin >= 10: score += 5
    elif ebitda_margin > 0:   score -= 10
    else:                     score -= 30

    fcf_margin = (fcf / revenue * 100.0) if revenue > 0 else 0
    if fcf_margin >= 20: score += 15
    elif fcf_margin >= 10: score += 8
    elif fcf_margin < 0:   score -= 20

    if yoy_growth >= 10: score += 10
    elif yoy_growth >= 0:  score += 3
    elif yoy_growth < -5:  score -= 15

    score = max(0, min(100, int(round(score))))
    return score, f"EBITDA margin {ebitda_margin:.1f}%, FCF conversion {fcf_margin:.1f}%, growth {yoy_growth:.1f}%"


def score_governance(governance: dict | None) -> tuple[int, str]:
    """Lower defenses + cleaner board → easier to take private."""
    if not governance:
        return 50, "Governance data unavailable"

    score = 60.0
    feasibility = str(governance.get("feasibility_assessment", "")).lower()
    if feasibility == "easy":      score += 30
    elif feasibility == "moderate": score += 10
    elif feasibility == "difficult": score -= 25

    defense = str(governance.get("takeover_defense_strength", "")).lower()
    if defense == "low":     score += 10
    elif defense == "high":  score -= 15

    if governance.get("dual_class_shares") is True: score -= 15
    if governance.get("staggered_board") is True:   score -= 10
    if governance.get("poison_pill") is True:       score -= 10

    score = max(0, min(100, int(round(score))))
    return score, f"Feasibility: {governance.get('feasibility_assessment', 'unknown')}, Defense: {governance.get('takeover_defense_strength', 'unknown')}"


def score_risk_profile(risk: dict | None) -> tuple[int, str]:
    """Fewer high-severity risks → safer LBO."""
    if not risk:
        return 50, "Risk data unavailable"

    high = int(_safe_float(risk.get("high_severity_count")))
    if high == 0: score = 90
    elif high <= 2: score = 75
    elif high <= 4: score = 55
    elif high <= 6: score = 35
    else: score = 20

    return score, f"{high} high-severity risks identified"


def score_red_flags(red_flag: dict | None) -> tuple[int, str]:
    """Critical red flags = deal killers; lots of high = caution."""
    if not red_flag:
        return 70, "No red-flag scan available"

    critical = int(_safe_float(red_flag.get("deal_breakers_count")))
    high = int(_safe_float(red_flag.get("high_concern_count")))

    if critical >= 1: score = 10
    elif high >= 3:   score = 30
    elif high >= 1:   score = 55
    else:             score = 90

    return score, f"{critical} critical, {high} high-concern flags"


def score_sentiment(sentiment: dict | None) -> tuple[int, str]:
    """Confident management is good; defensive = bad."""
    if not sentiment:
        return 60, "Sentiment data unavailable"

    tone = str(sentiment.get("overall_tone", "")).lower()
    shift = str(sentiment.get("yoy_tone_shift", "")).lower()

    if tone == "confident": score = 80
    elif tone == "mixed":    score = 60
    elif tone == "cautious": score = 50
    elif tone == "defensive": score = 30
    else: score = 60

    if "negative" in shift: score -= 10
    elif "positive" in shift: score += 10

    score = max(0, min(100, int(round(score))))
    return score, f"Tone: {sentiment.get('overall_tone', 'unknown')}, shift: {sentiment.get('yoy_tone_shift', 'unknown')}"


def score_lbo_returns(lbo: dict | None) -> tuple[int, str]:
    """Higher modeled IRR → better."""
    if not lbo or lbo.get("status") != "ok":
        return 50, "LBO model could not be run"

    base_irr = _safe_float(lbo.get("summary", {}).get("irr_base_pct"))
    if base_irr >= 25:     score = 95
    elif base_irr >= 20:   score = 80
    elif base_irr >= 15:   score = 65
    elif base_irr >= 10:   score = 50
    elif base_irr >= 5:    score = 35
    else: score = 20

    return score, f"Base case IRR: {base_irr:.1f}%"


def compute_feasibility(
    financial: dict | None,
    governance: dict | None,
    risk: dict | None,
    red_flag: dict | None,
    sentiment: dict | None,
    lbo: dict | None,
) -> dict:
    weights = {
        "financial":   0.25,
        "lbo_returns": 0.25,
        "governance":  0.15,
        "risk":        0.15,
        "red_flags":   0.15,
        "sentiment":   0.05,
    }

    components = {}
    s1, r1 = score_financial_quality(financial); components["financial"] = (s1, r1)
    s2, r2 = score_lbo_returns(lbo);             components["lbo_returns"] = (s2, r2)
    s3, r3 = score_governance(governance);       components["governance"] = (s3, r3)
    s4, r4 = score_risk_profile(risk);           components["risk"] = (s4, r4)
    s5, r5 = score_red_flags(red_flag);          components["red_flags"] = (s5, r5)
    s6, r6 = score_sentiment(sentiment);         components["sentiment"] = (s6, r6)

    weighted = sum(components[k][0] * weights[k] for k in weights)
    overall = int(round(weighted))

    if overall >= 80:   grade, verdict = "A", "Highly Attractive Take-Private Target"
    elif overall >= 70: grade, verdict = "B", "Attractive Target — Proceed to IC"
    elif overall >= 60: grade, verdict = "C", "Marginal Target — Material Diligence Required"
    elif overall >= 50: grade, verdict = "D", "Weak Target — Significant Concerns"
    else:                grade, verdict = "F", "Pass — Fundamental Issues"

    return {
        "score": overall,
        "grade": grade,
        "verdict": verdict,
        "components": {
            k: {"score": components[k][0], "reason": components[k][1], "weight_pct": int(weights[k] * 100)}
            for k in weights
        },
    }
