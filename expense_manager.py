import json
import os
from datetime import datetime
from expense import Expense
from category import Category


class ExpenseManager:

    def __init__(self):
        self.expenses = []
        self.categories = []
        self.data_file = "expenses_data.json"

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.expenses.sort(key=lambda x: x.date, reverse=True)

    def remove_expense(self, expense):
        if expense in self.expenses:
            self.expenses.remove(expense)

    def add_category(self, category):
        self.categories.append(category)
        self.categories.sort(key=lambda x: x.name)

    def get_expenses_by_category(self, category):
        return [expense for expense in self.expenses if expense.category.name == category.name]

    def get_expenses_by_period(self, start_date, end_date):
        return [expense for expense in self.expenses
        if start_date <= expense.date <= end_date]

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def get_total_by_category(self, category):
        expenses = self.get_expenses_by_category(category)
        return sum(expense.amount for expense in expenses)

    def save_data(self):
        data = {
            "categories": [
                {"name": category.name} for category in self.categories
            ],
            "expenses": [
                {
                    "description": expense.description,
                    "amount": expense.amount,
                    "date": expense.date.strftime('%Y-%m-%d'),
                    "category": expense.category.name
                } for expense in self.expenses
            ]
        }

        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Помилка при збереженні даних: {e}")

    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.categories = []
            for cat_data in data.get("categories", []):
                category = Category(cat_data["name"])
                self.categories.append(category)

            self.expenses = []
            for exp_data in data.get("expenses", []):
                category_name = exp_data["category"]
                category = next((c for c in self.categories if c.name == category_name), None)

                if not category:
                    category = Category(category_name)
                    self.categories.append(category)

                date = datetime.strptime(exp_data["date"], '%Y-%m-%d').date()
                expense = Expense(
                    exp_data["description"],
                    exp_data["amount"],
                    date,
                    category
                )
                self.expenses.append(expense)

            self.expenses.sort(key=lambda x: x.date, reverse=True)
            self.categories.sort(key=lambda x: x.name)

        except Exception as e:
            print(f"Помилка при завантаженні даних: {e}")