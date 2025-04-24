from src.settings import model
from src.models.date_range import DateRange

from json import loads
from datetime import datetime, date

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

Тебе нужно извлечь даты строго в формате DD-MM-YYYY, а также записать запрос без даты.
"""


def get_date_range_from_query(query: str) -> DateRange:
    """
    Extracts a date range from a query string using a language model.
    Args:
        query: The query string containing the date range.
    Returns:
        DateRange object containing the start and end dates.
    """
    response = model.configure(response_format=DateRange).run([
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": query}
    ])

    response_data = loads(response.text)
    start_date = parse_date(response_data['start_date'])
    end_date = parse_date(response_data['end_date'])

    return DateRange(start_date=start_date, end_date=end_date,
                     query_without_date=response_data['query_without_date'])


def parse_date(date_str: str) -> date:
    """
    Parses a date string in the format DD-MM-YYYY.
    Args:
        date_str: The date string to parse.
    Returns:
        A datetime object representing the parsed date.
    """
    parts_len = tuple(map(len, date_str.split("-")))
    if parts_len == (2, 2, 4):
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    elif parts_len == (4, 2, 2):
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    raise ValueError(f"Invalid date format: {date_str}")


def main():
    query = "Как развивалась наука в марте 1935 года"
    date_range = get_date_range_from_query(query)
    print(f"Start Date: {date_range.start_date}")
    print(f"End Date: {date_range.end_date}")
    print(f"Query:", date_range.query_without_date)


if __name__ == '__main__':
    main()
