"""Generates the partner-ready IC memo as a PDF."""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def build_ic_memo_pdf(output_path: str, content: dict) -> str:
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(f"Investment Committee Memo — {content.get('company_name', 'Target')}", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Ticker: {content.get('ticker')}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Executive Summary", styles["Heading1"]),
        Paragraph(content.get("exec_summary", "TBD"), styles["BodyText"]),
        # TODO: add full sections
    ]
    doc.build(story)
    return output_path
