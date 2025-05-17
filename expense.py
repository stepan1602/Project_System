from utils.validators import validate_amount, validate_text_field

class Expense:
    def __init__(self, description, amount, date, category):
        validate_text_field(description, "Опис")

        if isinstance(amount, str):
            amount = validate_amount(amount)

        self.description = description
        self.amount = amount
        self.date = date
        self.category = category

    def __str__(self):
        return f"{self.date} - {self.description}: {self.amount:.2f} ({self.category.name})"