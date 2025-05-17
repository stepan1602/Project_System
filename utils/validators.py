import datetime
from .exceptions import ValidationError


def validate_text_field(text, field_name):

    if not text or not text.strip():
        raise ValidationError(f"{field_name} не може бути порожнім")

    if len(text) > 100:
        raise ValidationError(f"{field_name} не може бути довшим за 100 символів")

    return text.strip()


def validate_amount(amount_str):
    try:
        amount_str = amount_str.replace(',', '.')
        amount = float(amount_str)

        if amount <= 0:
            raise ValidationError("Сума повинна бути більше нуля")

        return amount
    except ValueError:
        raise ValidationError("Сума має бути числом")


def validate_date(date_str):
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        today = datetime.date.today()
        if date > today:
            raise ValidationError("Дата не може бути в майбутньому")

        return date
    except ValueError:
        raise ValidationError("Неправильний формат дати. Використовуйте формат YYYY-MM-DD")