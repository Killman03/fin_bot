import datetime

# Dictionary to map Russian month names to month numbers
MONTH_NAMES = {
    'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6,
    'Июль': 7, 'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
}


def is_valid_date(day, month, year):
    try:
        month_number = MONTH_NAMES[month]
        datetime.datetime(year, month_number, day)
        return True
    except (ValueError, KeyError):
        return False
