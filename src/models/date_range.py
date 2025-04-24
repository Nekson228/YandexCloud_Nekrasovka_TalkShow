from pydantic import BaseModel, Field
from datetime import date


class DateRange(BaseModel):
    start_date: date = Field(description="Начальная дата")
    end_date: date = Field(description="Конечная дата")
    query_without_date: str = Field(description="Запрос пользователя без даты")

    def format_query(self) -> str:
        date_formater = "%d-%m-%Y"
        if self.start_date == self.end_date:
            return (f"{self.query_without_date} в "
                    f"{self.start_date.strftime(date_formater)}")
        return (f"{self.query_without_date} c "
                f"{self.start_date.strftime(date_formater)} по "
                f"{self.end_date.strftime(date_formater)}")
