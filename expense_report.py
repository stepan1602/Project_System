class ExpenseReport:
    def __init__(self, expenses):
        self.expenses = expenses

    def get_total(self):
        return sum(expense.amount for expense in self.expenses)

    def get_category_totals(self):
        category_totals = {}

        for expense in self.expenses:
            category_name = expense.category.name
            if category_name not in category_totals:
                category_totals[category_name] = 0

            category_totals[category_name] += expense.amount

        return category_totals

    def get_category_percentages(self):
        category_totals = self.get_category_totals()
        total = self.get_total()

        category_percentages = {}
        if total > 0:
            for category, amount in category_totals.items():
                category_percentages[category] = (amount / total) * 100

        return category_percentages

    def print_expenses(self):
        if not self.expenses:
            print("Немає витрат для відображення.")
            return

        print(f"{'Дата':<12}{'Опис':<30}{'Сума':<10}{'Категорія':<20}")
        print("-" * 72)

        for expense in self.expenses:
            date_str = expense.date.strftime('%Y-%m-%d')
            print(f"{date_str:<12}{expense.description[:30]:<30}{expense.amount:<10.2f}{expense.category.name:<20}")