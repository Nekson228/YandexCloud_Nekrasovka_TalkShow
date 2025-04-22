from src.settings import model
from src.models.date_range import DateRange

from json import loads
from datetime import datetime

system_prompt = """
Ты — помощник по нормализации временных периодов. 
Твоя задача — из пользовательского запроса выделить временной диапазон.
**Правила:**
1. Если указано:
   - "в 1930 году" → верни "1930-01-01" и "1930-12-31"
   - "в сентябре 1935 года" → "1935-09-01" и "1935-09-30"
   - "в течение 1925 года" → то же, что и "в 1925 году"
   - "с 1925 по 1930 годы" → "1925-01-01" и "1930-12-31"
   - "летом 1932" — интерпретируй как "1932-06-01" — "1932-08-31"
   - "в первой половине марта 1941 года" — определи как "1941-03-01" — "1941-03-15"
2. Всегда используй **первые и последние календарные даты** в соответствующем диапазоне.
3. Если в запросе несколько дат — выбери главный интервал.
4. Тебе нужно извлечь даты в формате DD-MM-YYYY.
"""


def get_date_range_from_query(query: str) -> DateRange:
    """
    Extracts a date range from a query string using a language model.
    Args:
        query (str): The query string containing the date range.
    Returns:
        DateRange: An object containing the start and end dates.
    """
    response = model.configure(response_format=DateRange).run([
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": query}
    ])

    response_data = loads(response.text)
    start_date = datetime.strptime(response_data['start_date'], "%d-%m-%Y").date()
    end_date = datetime.strptime(response_data['end_date'], "%d-%m-%Y").date()

    return DateRange(start_date=start_date, end_date=end_date)


def main():
    query = "Как развивалась наука в марте 1935 года"
    date_range = get_date_range_from_query(query)
    print(f"Start Date: {date_range.start_date}")
    print(f"End Date: {date_range.end_date}")


if __name__ == '__main__':
    main()
