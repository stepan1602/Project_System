from utils.validators import validate_text_field

class Category:

    def __init__(self, name):
        validate_text_field(name, "Назва категорії")
        self.name = name

    def __str__(self):
        return self.name