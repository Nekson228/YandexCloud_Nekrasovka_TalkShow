from pydantic import BaseModel, Field
from datetime import date


class DateRange(BaseModel):
    start_date: date = Field(description="Начальная дата")
    end_date: date = Field(description="Конечная дата")
