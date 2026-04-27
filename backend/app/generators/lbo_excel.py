"""Generates a fully-linked LBO model in Excel."""
from openpyxl import Workbook


def build_lbo_excel(output_path: str, model_inputs: dict) -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = "LBO Model"
    ws["A1"] = "DiligenceAI — LBO Model"
    ws["A3"] = "Entry EV"
    ws["B3"] = model_inputs.get("entry_ev", 0)
    # TODO: build Sources & Uses, Debt Schedule, Returns Waterfall, Sensitivity
    wb.save(output_path)
    return output_path
