def format_days_passed(days: int) -> str:
    """
    Форматирует количество дней в человекочитаемую строку 
    со склонениями.
    """
    if days == 0:
        return "сегодня"
    
    # Последняя цифра
    last_digit = days % 10
    # Две последние цифры для исключений 11-19
    last_two_digits = days % 100

    if last_two_digits in {11, 12, 13, 14}:
        return f"{days} дней назад"
    
    if last_digit == 1:
        return f"{days} день назад"
    
    if last_digit in {2, 3, 4}:
        return f"{days} дня назад"
        
    return f"{days} дней назад"

