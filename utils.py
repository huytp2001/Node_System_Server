from datetime import datetime, timedelta

def get_format_date(reverse_day):
    current_date = datetime.now()
    new_date = current_date - timedelta(days=reverse_day)
    day = new_date.day
    month = new_date.month
    formatted_date = "{:02d}-{:02d}".format(day, month)
    return formatted_date

