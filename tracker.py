from database import Database

class Tracker:
    def __init__(self, host, user, password, database):
        self.database = Database(host, user, password, database)

    def add_expense(self, expense, amount, category, income, savings):
        self.database.add_expense( expense, amount, category, income, savings)

    def delete_expense(self, expense_id):
        self.database.delete_expense(expense_id)

    def get_expenses(self):
        return self.database.get_expenses()

    def get_expenses_by_month_year(self, month, year):
        return self.database.get_expenses_by_month_year(month, year)

    def close_connection(self):
        self.database.close_connection()




""" 
from database import Database class Tracker: def __init__(self, host, user, password, database): self.database = Database(host, user, password, database) def add_expense(self, expense, amount, category, income, savings): self.database.add_expense(expense, amount, category, income, savings) def delete_expense(self, expense_id): self.database.delete_expense(expense_id) def get_expenses(self): return self.database.get_expenses() def get_expenses_by_month_year(self, month, year): return self.database.get_expenses_by_month_year(month, year) def close_connection(self): self.database.close_connection(

"""