"""Investment Committee memo PDF generator (reportlab)."""
import os
from datetime import datetime
from html import escape as _html_escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def _safe(text: str) -> str:
    """Escape text for reportlab Paragraph (handles &, <, >).

    Preserves existing <b>, <i>, <font> tags by escaping other ampersands only.
    """
    if text is None:
        return ""
    s = str(text)
    # Replace & not followed by amp; lt; gt; etc with &amp;
    import re
    return re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', s)


def _money(v, prefix="$") -> str:
    if v is None:
        return "—"
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    if abs(v) >= 1000:
        return f"{prefix}{v / 1000:,.1f}B"
    return f"{prefix}{v:,.0f}M"


def _pct(v) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):.1f}%"
    except (TypeError, ValueError):
        return str(v)


def generate_ic_memo_pdf(
    ticker: str,
    company_name: str,
    output_dir: str,
    financial: dict,
    commercial: dict,
    risk: dict,
    governance: dict,
    market: dict,
    sentiment: dict,
    red_flag: dict,
    lbo: dict,
    feasibility: dict,
    synthesis: dict,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{ticker}_IC_Memo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        filepath, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"], fontSize=22,
        textColor=colors.HexColor("#0a2540"), spaceAfter=8, alignment=TA_LEFT,
    )
    h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=14,
        textColor=colors.HexColor("#0a2540"), spaceBefore=12, spaceAfter=6,
    )
    h3 = ParagraphStyle(
        "H3", parent=styles["Heading3"], fontSize=11,
        textColor=colors.HexColor("#1a73e8"), spaceBefore=8, spaceAfter=4,
    )
    body = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=6,
    )
    body_small = ParagraphStyle(
        "BodySmall", parent=styles["Normal"], fontSize=9, leading=12, spaceAfter=4,
        textColor=colors.HexColor("#444"),
    )
    bullet_style = ParagraphStyle(
        "Bullet", parent=body, leftIndent=18, bulletIndent=6, spaceAfter=3,
    )
    score_num_style = ParagraphStyle(
        "ScoreNum", parent=styles["Normal"], fontSize=22, leading=24,
        alignment=TA_CENTER,
    )

    story = []

    # ------- HEADER -------
    story.append(Paragraph("INVESTMENT COMMITTEE MEMO", title_style))
    story.append(Paragraph(
        f"<b>{_safe(company_name)} ({ticker})</b> &nbsp;|&nbsp; "
        f"Take-Private Screening &nbsp;|&nbsp; "
        f"{datetime.now().strftime('%B %d, %Y')}",
        body_small,
    ))
    story.append(Spacer(1, 0.2 * inch))

    # ------- SCORE BOX (with wider score column to prevent line break) -------
    score = feasibility.get("score", 0)
    grade = feasibility.get("grade", "?")
    verdict = feasibility.get("verdict", "")
    score_color_hex = (
        "#0d9f4f" if score >= 70 else
        "#f59e0b" if score >= 50 else
        "#dc2626"
    )

    score_table = Table(
        [[
            Paragraph("<b>FEASIBILITY<br/>SCORE</b>", body_small),
            Paragraph(
                f"<font size='22' color='{score_color_hex}'><b>{score}/100</b></font>",
                score_num_style,
            ),
            Paragraph(f"<b>Grade {grade}</b>", body),
            Paragraph(f"<i>{_safe(verdict)}</i>", body),
        ]],
        colWidths=[1.0 * inch, 1.6 * inch, 0.9 * inch, 3.2 * inch],  # widened score col
    )
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f7fa")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.2 * inch))

    # ------- EXECUTIVE SUMMARY -------
    story.append(Paragraph("Executive Summary", h2))
    story.append(Paragraph(_safe(synthesis.get("executive_summary", "Synthesis not available.")), body))

    rec = synthesis.get("recommendation", "—")
    rec_color = ("#0d9f4f" if "PROCEED TO IC" in rec else
                 "#f59e0b" if "CAVEATS" in rec else "#dc2626")
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        f"<b>Recommendation:</b> <font color='{rec_color}'><b>{_safe(rec)}</b></font>",
        body,
    ))
    story.append(Paragraph(_safe(synthesis.get("recommendation_rationale", "")), body_small))

    # ------- SIZE-PROHIBITIVE WARNING -------
    if lbo and lbo.get("size_prohibitive"):
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(
            f"<b><font color='#f59e0b'>⚠ Size Note:</font></b> "
            f"<i>{_safe(lbo.get('size_prohibitive_note', ''))}</i>",
            body_small,
        ))

    # ------- HEADLINE METRICS -------
    story.append(Paragraph("Headline Metrics", h2))

    pe = market.get("pe_ratio")
    ev_eb = market.get("ev_to_ebitda")

    headline_data = [
        ["", f"FY{financial.get('fiscal_year', '—')}"],
        ["Revenue", _money(financial.get("revenue_usd_millions"))],
        ["EBITDA", _money(financial.get("ebitda_usd_millions"))],
        ["EBITDA Margin", _pct(financial.get("ebitda_margin_pct"))],
        ["Net Income", _money(financial.get("net_income_usd_millions"))],
        ["Free Cash Flow", _money(financial.get("free_cash_flow_usd_millions"))],
        ["Total Debt", _money(financial.get("total_debt_usd_millions"))],
        ["Cash & Equivalents", _money(financial.get("cash_and_equivalents_usd_millions"))],
        ["Revenue Growth (YoY)", _pct(financial.get("revenue_growth_yoy_pct"))],
        ["Market Cap", _money(market.get("market_cap_usd_millions"))],
        ["Enterprise Value", _money(market.get("ev_usd_millions"))],
        ["P/E Ratio", f"{pe:.1f}x" if isinstance(pe, (int, float)) else "—"],
        ["EV / EBITDA", f"{ev_eb:.1f}x" if isinstance(ev_eb, (int, float)) else "—"],
    ]
    metrics_table = Table(headline_data, colWidths=[2.2 * inch, 2.2 * inch])
    metrics_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a2540")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)

    # ------- INVESTMENT THESIS -------
    story.append(PageBreak())
    story.append(Paragraph("Investment Thesis", h2))
    for bullet in synthesis.get("investment_thesis", []) or []:
        story.append(Paragraph(f"• {_safe(bullet)}", bullet_style))

    story.append(Paragraph("Value Creation Levers", h3))
    for bullet in synthesis.get("value_creation_levers", []) or []:
        story.append(Paragraph(f"• {_safe(bullet)}", bullet_style))

    story.append(Paragraph("Key Risks to Thesis", h3))
    for bullet in synthesis.get("key_risks_to_thesis", []) or []:
        story.append(Paragraph(f"• {_safe(bullet)}", bullet_style))

    # ------- LBO RETURNS -------
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("LBO Returns Summary (Base / Bull / Bear)", h2))
    if lbo and lbo.get("status") == "ok":
        lbo_data = [
            ["Scenario", "IRR", "MOIC", "Exit Equity Value"],
            ["Base", _pct(lbo["base"]["returns"]["irr_pct"]),
             f"{lbo['base']['returns']['moic']:.2f}x",
             _money(lbo["base"]["exit"]["exit_equity_value_usd_millions"])],
            ["Bull", _pct(lbo["bull"]["returns"]["irr_pct"]),
             f"{lbo['bull']['returns']['moic']:.2f}x",
             _money(lbo["bull"]["exit"]["exit_equity_value_usd_millions"])],
            ["Bear", _pct(lbo["bear"]["returns"]["irr_pct"]),
             f"{lbo['bear']['returns']['moic']:.2f}x",
             _money(lbo["bear"]["exit"]["exit_equity_value_usd_millions"])],
        ]
        lbo_table = Table(lbo_data, colWidths=[1.2 * inch, 1.0 * inch, 1.0 * inch, 1.5 * inch])
        lbo_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a2540")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#fef3c7")),
            ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#dcfce7")),
            ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#fee2e2")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(lbo_table)
        sponsor_eq = lbo["base"]["inputs"]["sponsor_equity_at_close_usd_millions"]
        story.append(Paragraph(
            f"Base case: 4% revenue CAGR, modest margin expansion, 12.0x exit multiple. "
            f"Sponsor equity at entry: {_money(sponsor_eq)}. 55% leverage at close.",
            body_small,
        ))

    # ------- COMMERCIAL DEEP DIVE -------
    story.append(PageBreak())
    story.append(Paragraph("Commercial Diligence", h2))
    if commercial:
        if commercial.get("business_segments"):
            segs = ", ".join(str(x) for x in commercial["business_segments"][:8])
            story.append(Paragraph(f"<b>Segments:</b> {_safe(segs)}", body))
        if commercial.get("primary_products"):
            prods = ", ".join(str(x) for x in commercial["primary_products"][:6])
            story.append(Paragraph(f"<b>Products:</b> {_safe(prods)}", body))
        if commercial.get("key_competitors"):
            comps = ", ".join(str(x) for x in commercial["key_competitors"][:6])
            story.append(Paragraph(f"<b>Competitors:</b> {_safe(comps)}", body))
        story.append(Paragraph(
            f"<b>Customer concentration:</b> {_safe(commercial.get('customer_concentration', '—'))}",
            body,
        ))
        story.append(Paragraph(
            f"<b>Geographic mix:</b> {_safe(commercial.get('geographic_mix', '—'))}",
            body,
        ))
        story.append(Paragraph("Competitive Advantages", h3))
        for adv in commercial.get("competitive_advantages", []) or []:
            story.append(Paragraph(f"• {_safe(adv)}", bullet_style))
        story.append(Paragraph("Growth Strategy", h3))
        story.append(Paragraph(_safe(commercial.get("growth_strategy", "—")), body))
    else:
        story.append(Paragraph("Commercial agent did not return data for this run.", body_small))

    # ------- RISKS -------
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Top Risks", h2))
    if risk and risk.get("top_risks"):
        for r in risk["top_risks"]:
            sev = str(r.get("severity", "—"))
            sev_color = ("#dc2626" if sev.lower() == "high" else
                         "#f59e0b" if sev.lower() == "medium" else "#0d9f4f")
            story.append(Paragraph(
                f"<b>{_safe(r.get('risk', '—'))}</b> "
                f"<font color='{sev_color}'><b>[{sev}]</b></font> "
                f"<i>({_safe(r.get('category', '—'))})</i>",
                body,
            ))
            story.append(Paragraph(_safe(r.get("description", "")), body_small))
    else:
        story.append(Paragraph("Risk agent did not return data for this run.", body_small))

    # ------- GOVERNANCE -------
    story.append(PageBreak())
    story.append(Paragraph("Governance Assessment", h2))
    if governance:
        gov_rows = [
            ["Board Size", str(governance.get("board_size", "—") or "—")],
            ["Independent Directors %", _pct(governance.get("independent_directors_pct"))],
            ["CEO/Chair Combined", str(governance.get("ceo_chair_combined", "—") or "—")],
            ["Staggered Board", str(governance.get("staggered_board", "—") or "—")],
            ["Poison Pill", str(governance.get("poison_pill", "—") or "—")],
            ["Dual-Class Shares", str(governance.get("dual_class_shares", "—") or "—")],
            ["Insider Ownership %", _pct(governance.get("insider_ownership_pct"))],
            ["Largest Holder", str(governance.get("largest_holder", "—") or "—")],
            ["Defense Strength", str(governance.get("takeover_defense_strength", "—") or "—")],
            ["Take-Private Feasibility", str(governance.get("feasibility_assessment", "—") or "—")],
        ]
        gov_table = Table(gov_rows, colWidths=[2.2 * inch, 2.5 * inch])
        gov_table.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(gov_table)
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(_safe(governance.get("summary", "")), body))

    # ------- RED FLAGS -------
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Red-Flag Scan (Recent 8-Ks)", h2))
    if red_flag and red_flag.get("red_flags"):
        for f in red_flag["red_flags"]:
            sev = str(f.get("severity", "—"))
            sev_color = ("#dc2626" if sev.lower() in ("critical", "high") else
                         "#f59e0b" if sev.lower() == "medium" else "#0d9f4f")
            story.append(Paragraph(
                f"<b>{_safe(f.get('flag', '—'))}</b> "
                f"<font color='{sev_color}'><b>[{sev}]</b></font> "
                f"<i>{_safe(f.get('category', '—'))} — {_safe(f.get('filing_date', ''))}</i>",
                body,
            ))
            story.append(Paragraph(_safe(f.get("description", "")), body_small))
    else:
        story.append(Paragraph("No material red flags identified.", body))

    # ------- MANAGEMENT TONE -------
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Management Tone Analysis", h2))
    if sentiment and sentiment.get("overall_tone"):
        story.append(Paragraph(
            f"<b>Overall tone:</b> {_safe(sentiment.get('overall_tone', '—'))} &nbsp; "
            f"<b>YoY shift:</b> {_safe(sentiment.get('yoy_tone_shift', '—'))}",
            body,
        ))
        story.append(Paragraph(_safe(sentiment.get("summary", "")), body_small))
    else:
        story.append(Paragraph("Sentiment agent did not return data for this run.", body_small))

    # ------- FEASIBILITY BREAKDOWN -------
    story.append(PageBreak())
    story.append(Paragraph("Feasibility Score Breakdown", h2))
    components = feasibility.get("components", {}) or {}
    fb_rows = [["Dimension", "Score", "Weight", "Driver"]]
    for k, v in components.items():
        fb_rows.append([
            k.replace("_", " ").title(),
            f"{v.get('score', 0)}/100",
            f"{v.get('weight_pct', 0)}%",
            v.get("reason", "—"),
        ])
    fb_table = Table(fb_rows, colWidths=[1.5 * inch, 0.8 * inch, 0.7 * inch, 3.7 * inch])
    fb_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a2540")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ]))
    story.append(fb_table)

    # ------- NEXT STEPS -------
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Recommended Next Steps", h2))
    for s in synthesis.get("next_steps", []) or []:
        story.append(Paragraph(f"• {_safe(s)}", bullet_style))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "<i>Generated by DiligenceAI — agentic AI multi-agent analysis pipeline. "
        "Based on SEC EDGAR filings + market data. Not investment advice.</i>",
        body_small,
    ))

    doc.build(story)
    return filepath
