import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Poilkjmnb"
        )
        self.cursor = self.connection.cursor()
        self.create_database(database)
        self.connection.database = database
        self.create_expenses_table()

    def create_database(self, database):
        try:
            query = f"CREATE DATABASE IF NOT EXISTS {database}"
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(f"Failed to create database: {err}")
            self.connection.close()
            exit(1)

    def create_expenses_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                expense VARCHAR(255),
                amount FLOAT,
                category VARCHAR(255),
                income FLOAT,
                savings FLOAT,  # New savings column
                month INT,
                year INT
            )
        """
        self.cursor.execute(query)

    def add_expense(self, expense, amount, category, income, savings):
        now = datetime.now()
        month = now.month
        year = now.year
        query = "INSERT INTO expenses (expense, amount, category, income, savings, month, year) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (expense, amount, category, income, savings, month, year))
        self.connection.commit()

    def delete_expense(self, expense_id):
        query = "DELETE FROM expenses WHERE id = %s"
        self.cursor.execute(query, (expense_id,))
        self.connection.commit()

    def get_expenses(self):
        query = "SELECT * FROM expenses"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_expenses_by_month_year(self, month, year):
        query = "SELECT * FROM expenses WHERE month = %s AND year = %s"
        self.cursor.execute(query, (month, year))
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()