import re
from datetime import datetime, timedelta
from typing import Tuple, Optional

# Обновленное регулярное выражение: ищет либо дату, либо ключевые слова
# re.UNICODE позволяет \b корректно работать с кириллицей
DATE_REGEX = re.compile(
    r"\b((?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4}))\b|"
    r"\b(?P<today>сегодня)\b|"
    r"\b(?P<yesterday>вчера)\b",
    re.IGNORECASE | re.UNICODE
)

def parse_add_command(text: str) -> Tuple[str, Optional[datetime]]:
    """
    Парсит текст команды /add, извлекая название события и дату.
    Ключевые слова 'сегодня' и 'вчера' преобразуются в соответствующий datetime.

    :param text: Текст, идущий после команды /add.
    :return: Кортеж из (название_события, дата_или_None).
    """
    match = DATE_REGEX.search(text.strip())
    
    event_name = text.strip()
    event_date = None

    if match:
        # Вся найденная подстрока (дата или слово)
        full_match_text = match.group(0)
        
        # Сначала пытаемся извлечь дату
        try:
            if match.group("today"):
                event_date = datetime.now()
            elif match.group("yesterday"):
                event_date = datetime.now() - timedelta(days=1)
            elif match.group("day"): # Если нашлась группа с числом, месяцем, годом
                day = int(match.group("day"))
                month = int(match.group("month"))
                year_str = match.group("year")
                
                if len(year_str) == 2:
                    year = 2000 + int(year_str)
                else:
                    year = int(year_str)
                
                # Попытка создать datetime, которая валидирует дату
                event_date = datetime(year, month, day)

            # Если дата была успешно определена, удаляем ее из названия
            if event_date:
                event_name = DATE_REGEX.sub("", text).strip()

        except ValueError:
            # Если, например, дата 32.13.2025 - она невалидна.
            # Оставляем ее как часть названия, event_date остается None.
            event_date = None
            event_name = text.strip()

    return event_name, event_date
