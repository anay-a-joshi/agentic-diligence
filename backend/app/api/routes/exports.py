"""Serves generated PDF / Excel files."""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# The orchestrator writes files to backend/generated_outputs
OUTPUT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "generated_outputs"
))


@router.get("/downloads/{filename}")
async def download_file(filename: str):
    """Serve a generated PDF or Excel file."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail=f"File not found at {filepath}",
        )
    media_type = (
        "application/pdf" if filename.endswith(".pdf")
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if filename.endswith(".xlsx")
        else "application/octet-stream"
    )
    return FileResponse(filepath, media_type=media_type, filename=filename)
