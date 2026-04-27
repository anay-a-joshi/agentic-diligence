from pydantic import BaseModel
from datetime import date


class Filing(BaseModel):
    form_type: str
    filed_date: date
    accession_number: str
    url: str
