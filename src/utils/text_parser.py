import re
from datetime import datetime, timedelta
from typing import Tuple, Optional

# Регулярное выражение для поиска даты в конце строки.
# Поддерживает форматы: ДД.ММ.ГГГГ, ДД.ММ.ГГ, ДД.ММ.YYYY, ДД.ММ.YY
# А также ключевые слова "сегодня" и "вчера".
DATE_REGEX = re.compile(
    r"((?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4}))|(?P<today>сегодня)|(?P<yesterday>вчера)$",
    re.IGNORECASE
)

def parse_add_command(text: str) -> Tuple[str, Optional[datetime]]:
    """
    Парсит текст команды /add, извлекая название события и дату.

    :param text: Текст, идущий после команды /add.
    :return: Кортеж из (название_события, дата_или_None).
    """
    match = DATE_REGEX.search(text.strip())
    
    event_name = text.strip()
    event_date = None

    if match:
        full_match_text = match.group(0)
        # Удаляем найденную дату из названия события
        event_name = text.replace(full_match_text, "").strip()

        if match.group("today"):
            event_date = datetime.now()
        elif match.group("yesterday"):
            event_date = datetime.now() - timedelta(days=1)
        else:
            day = int(match.group("day"))
            month = int(match.group("month"))
            year_str = match.group("year")
            
            if len(year_str) == 2:
                # Для формата 'ГГ' считаем, что это 20xx год
                year = 2000 + int(year_str)
            else:
                year = int(year_str)
            
            try:
                # Валидация даты на корректность (например, 32.13.2025)
                event_date = datetime(year, month, day)
            except ValueError:
                # Если дата некорректна, она остается частью названия
                event_date = None
                event_name = text.strip()

    return event_name, event_date
