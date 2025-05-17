from expense_manager import ExpenseManager
from expense import Expense
from category import Category
from expense_report import ExpenseReport
from utils.validators import validate_amount, validate_date, validate_text_field
from utils.exceptions import ValidationError

import datetime
import os


class ExpenseManagementSystem:

    def __init__(self):
        self.expense_manager = ExpenseManager()
        self.running = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("_" * 50)
        print("-------|   СИСТЕМА УПРАВЛІННЯ ВИТРАТАМИ   |-------")
        print("_" * 50)
        print()

    def display_menu(self):
        self.clear_screen()
        self.print_header()
        print("Меню:")
        print("1. Додати нову витрату")
        print("2. Додати нову категорію")
        print("3. Переглянути всі витрати")
        print("4. Переглянути витрати за категорією")
        print("5. Переглянути витрати за період")
        print("6. Видалити витрату")
        print("7. Статистика витрат")
        print("8. Вийти з програми")
        print()

    def start(self):
        self.running = True

        self.expense_manager.load_data()

        while self.running:
            self.display_menu()
            choice = input("Виберіть опцію (1-8): ")

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.add_category()
            elif choice == '3':
                self.show_all_expenses()
            elif choice == '4':
                self.show_expenses_by_category()
            elif choice == '5':
                self.show_expenses_by_period()
            elif choice == '6':
                self.remove_expense()
            elif choice == '7':
                self.show_statistics()
            elif choice == '8':
                self.exit_program()
            else:
                input("Невірний вибір! Натисніть Enter, щоб продовжити...")

    def add_expense(self):
        self.clear_screen()
        self.print_header()
        print("ДОДАВАННЯ НОВОЇ ВИТРАТИ")
        print("-" * 50)

        if not self.expense_manager.categories:
            print("Спочатку створіть хоча б одну категорію!")
            input("[Натисніть Enter, для продовження]")
            return

        try:
            description = input("Опис витрати: ")
            validate_text_field(description, "Опис")

            amount_str = input("Сума витрати: ")
            amount = validate_amount(amount_str)

            date_str = input("Дата витрати (YYYY-MM-DD), або пусто для поточної дати: ")
            if date_str.strip():
                date = validate_date(date_str)
            else:
                date = datetime.date.today()

            print("\nДоступні категорії:")
            for i, category in enumerate(self.expense_manager.categories, 1):
                print(f"{i}. {category.name}")

            category_idx = int(input("\nВиберіть номер категорії: ")) - 1
            if 0 <= category_idx < len(self.expense_manager.categories):
                category = self.expense_manager.categories[category_idx]

                expense = Expense(description, amount, date, category)
                self.expense_manager.add_expense(expense)

                print("\nВитрату успішно додано!")
            else:
                print("\nНевірний номер категорії!")

        except ValidationError as e:
            print(f"\nПомилка: {e}")
        except ValueError as e:
            print(f"\nПомилка: {e}")

        input("\n[Натисніть Enter, для продовження]")

    def add_category(self):
        self.clear_screen()
        self.print_header()
        print("ДОДАВАННЯ НОВОЇ КАТЕГОРІЇ")
        print("-" * 50)

        try:
            name = input("Назва категорії: ")
            validate_text_field(name, "Назва категорії")

            if any(category.name.lower() == name.lower() for category in self.expense_manager.categories):
                print("\nКатегорія з такою назвою вже існує.")
            else:
                category = Category(name)
                self.expense_manager.add_category(category)
                print("\nКатегорію успішно додано!")

        except ValidationError as e:
            print(f"\nПомилка: {e}")

        input("\n[Натисніть Enter, для продовження]")

    def show_all_expenses(self):
        self.clear_screen()
        self.print_header()
        print("СПИСОК ВСІХ ВИТРАТ")
        print("-" * 50)

        if not self.expense_manager.expenses:
            print("Немає збережених витрат.")
        else:
            report = ExpenseReport(self.expense_manager.expenses)
            report.print_expenses()
            print(f"\nЗагальна сума витрат: {report.get_total():.2f}")

        input("\n[Натисніть Enter, для продовження]")

    def show_expenses_by_category(self):
        self.clear_screen()
        self.print_header()
        print("ВИТРАТИ ЗА КАТЕГОРІЄЮ")
        print("-" * 50)

        if not self.expense_manager.categories:
            print("Немає доступних категорій.")
            input("\n[Натисніть Enter, для продовження]")
            return

        print("Доступні категорії:")
        for i, category in enumerate(self.expense_manager.categories, 1):
            print(f"{i}. {category.name}")

        try:
            category_idx = int(input("\nВиберіть номер категорії: ")) - 1
            if 0 <= category_idx < len(self.expense_manager.categories):
                category = self.expense_manager.categories[category_idx]

                expenses = [exp for exp in self.expense_manager.expenses if exp.category.name == category.name]

                if not expenses:
                    print(f"\nНемає витрат у категорії '{category.name}'.")
                else:
                    print(f"\nВитрати у категорії '{category.name}':")
                    report = ExpenseReport(expenses)
                    report.print_expenses()
                    print(f"\nЗагальна сума витрат у категорії: {report.get_total():.2f}")
            else:
                print("\nНевірний номер категорії!")

        except ValueError:
            print("\nПомилка: введіть коректний номер категорії!")

        input("\n[Натисніть Enter, для продовження]")

    def show_expenses_by_period(self):
        self.clear_screen()
        self.print_header()
        print("ВИТРАТИ ЗА ПЕРІОД")
        print("-" * 50)

        if not self.expense_manager.expenses:
            print("Немає збережених витрат.")
            input("\n[Натисніть Enter, для продовження]")
            return

        try:
            print("Введіть початкову дату періоду (YYYY-MM-DD):")
            start_date_str = input("> ")
            start_date = validate_date(start_date_str)

            print("Введіть кінцеву дату періоду (YYYY-MM-DD):")
            end_date_str = input("> ")
            end_date = validate_date(end_date_str)

            if start_date > end_date:
                print("\nПомилка: початкова дата повинна бути раніше або дорівнювати кінцевій")
            else:
                expenses = [exp for exp in self.expense_manager.expenses
                            if start_date <= exp.date <= end_date]

                if not expenses:
                    print(f"\nНемає витрат за період з {start_date} по {end_date}.")
                else:
                    print(f"\nВитрати за період з {start_date} по {end_date}:")
                    report = ExpenseReport(expenses)
                    report.print_expenses()
                    print(f"\nЗагальна сума витрат за період: {report.get_total():.2f}")

        except ValidationError as e:
            print(f"\nПомилка: {e}")

        input("\n[Натисніть Enter, для продовження]")

    def remove_expense(self):
        self.clear_screen()
        self.print_header()
        print("ВИДАЛЕННЯ ВИТРАТИ")
        print("-" * 50)

        if not self.expense_manager.expenses:
            print("Немає збережених витрат для видалення.")
            input("\n[Натисніть Enter, для продовження]")
            return

        print("Список витрат:")
        for i, expense in enumerate(self.expense_manager.expenses, 1):
            print(f"{i}. {expense.date} - {expense.description} ({expense.amount:.2f}, {expense.category.name})")

        try:
            expense_idx = int(input("\nВведіть номер витрати для видалення: ")) - 1

            if 0 <= expense_idx < len(self.expense_manager.expenses):
                expense = self.expense_manager.expenses[expense_idx]
                self.expense_manager.remove_expense(expense)
                print("\nВитрату успішно видалено!")
            else:
                print("\nНевірний номер витрати!")

        except ValueError:
            print("\nПомилка: введіть коректний номер витрати!")

        input("\n[Натисніть Enter, для продовження]")

    def show_statistics(self):
        self.clear_screen()
        self.print_header()
        print("СТАТИСТИКА ВИТРАТ")
        print("-" * 50)

        if not self.expense_manager.expenses:
            print("Немає збережених витрат для аналізу.")
            input("\n[Натисніть Enter, для продовження]")
            return

        category_stats = {}
        total = 0.0

        for expense in self.expense_manager.expenses:
            category_name = expense.category.name
            if category_name not in category_stats:
                category_stats[category_name] = 0.0

            category_stats[category_name] += expense.amount
            total += expense.amount

        sorted_stats = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)

        print("Витрати за категоріями:")
        print("-" * 50)
        print(f"{'Категорія':<20}{'Сума':<15}{'Відсоток':<10}")
        print("-" * 50)

        for category_name, amount in sorted_stats:
            percentage = (amount / total) * 100 if total > 0 else 0
            print(f"{category_name:<20}{amount:<15.2f}{percentage:<10.2f}%")

        print("-" * 50)
        print(f"{'Загалом':<20}{total:<15.2f}{100:<10.2f}%")

        input("\n[Натисніть Enter, для продовження]")

    def exit_program(self):
        self.clear_screen()
        self.print_header()
        print("Збереження даних...")

        self.expense_manager.save_data()

        print("Дані успішно збережено!")
        print("\nДякую за користування програмою!")
        self.running = False
        input("\n[Натисніть Enter, для виходу]")


if __name__ == "__main__":
    system = ExpenseManagementSystem()
    system.start()