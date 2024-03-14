import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tracker import Tracker
import datetime
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    def __init__(self):
        self.tracker = Tracker("localhost", "your_username", "your_password", "project")
        self.transactions = []
        self.create_widgets()
        self.load_finance_tips()

    def load_finance_tips(self):
    # Calculate the total income and total expenses from the expenses list
        expenses = self.tracker.get_expenses()
        total_income = sum(expense[4] for expense in expenses)
        total_expenses = sum(expense[2] for expense in expenses)
        total_savings = sum(expense[5] for expense in expenses)

    # Generate finance tips based on the calculations
        tips = []
        if total_expenses > total_income:
            tips.append("Spending exceeded your income. Consider reducing expenses or increasing your income.")
        else:
            if total_income == 0:
                if total_savings == 0:
                    tips.append("You haven't recorded any income or savings yet.")
                else:
                    tips.append("You have savings but no income recorded. Please ensure your income is correctly recorded.")
            else:
                savings_percentage = (total_savings / total_income) * 100
                if savings_percentage < 10:
                    tips.append("Your savings are less than 10% of your income. Try to increase your savings rate.")
                elif savings_percentage < 20:
                    tips.append("Good job on saving! Aim for a savings rate of at least 20% of your income.")
                else:
                    tips.append("Excellent savings rate! Keep up the good work.")

        # Display the finance tips in the text widget
        tips_text = "\n".join(tips)
        self.tips_text.insert(tk.END, tips_text)
        #self.display_dashboard(total_income, total_expenses, total_savings)


    def display_dashboard(self, total_income, total_expenses, total_savings):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Display total expenses, total income, and total savings using matplotlib bar chart
        labels = ['Total Income', 'Total Expenses', 'Total Savings']
        values = [total_income, total_expenses, total_savings]

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot()

        ax.bar(labels, values, color=['green', 'red', 'blue'])
        ax.set_ylabel('Amount ($)')
        ax.set_title('Financial Overview')

        # Add value labels on top of each bar
        for i, v in enumerate(values):
            ax.text(i, v + max(values) * 0.02, f"${v:.2f}", ha='center', va='bottom')

        # Display the bar chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.dashboard_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_widgets(self):
        self.window = tk.Tk()
        self.window.title("Personal Finance Management")

        # Load and display the background image
        background_image = Image.open("background.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.window, image=background_photo)
        background_label.image = background_photo  # Keep a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create and configure your GUI widgets here
        style = ttk.Style()
        style.theme_use("clam")  # Use the "clam" theme
        style.configure("TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 12))
        style.configure("TButton", background="#4CAF50", foreground="#FFFFFF", font=("Arial", 12))
        style.configure("TEntry", fieldbackground="#F8F8F8", foreground="#333333", font=("Arial", 12))
        style.configure("TLabelframe.Label", font=("Arial", 14, "bold"))

        self.expense_label = ttk.Label(self.window, text="Expense:")
        self.expense_label.grid(row=0, column=0, padx=10, pady=5)
        self.expense_entry = ttk.Entry(self.window)
        self.expense_entry.grid(row=0, column=1, padx=10, pady=5)

        self.income_label = ttk.Label(self.window, text="Income:")
        self.income_label.grid(row=3, column=0, padx=10, pady=5)
        self.income_entry = ttk.Entry(self.window)
        self.income_entry.grid(row=3, column=1, padx=10, pady=5)

        self.savings_label = ttk.Label(self.window, text="Savings:")
        self.savings_label.grid(row=4, column=0, padx=10, pady=5)
        self.savings_entry = ttk.Entry(self.window)
        self.savings_entry.grid(row=4, column=1, padx=10, pady=5)

        self.amount_label = ttk.Label(self.window, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=5)
        self.amount_entry = ttk.Entry(self.window)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        self.category_label = ttk.Label(self.window, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=5)
        self.category_entry = ttk.Entry(self.window)
        self.category_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(self.window, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.expense_listbox = tk.Listbox(self.window, width=50, font=("Arial", 12))
        self.expense_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.delete_button = ttk.Button(self.window, text="Delete Expense", command=self.delete_expense)
        self.delete_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        self.filter_label = ttk.Label(self.window, text="Filter (Month/Year):")
        self.filter_label.grid(row=8, column=0, padx=10, pady=5)
        self.filter_entry = ttk.Entry(self.window)
        self.filter_entry.grid(row=8, column=1, padx=10, pady=5)
        self.filter_button = ttk.Button(self.window, text="Filter", command=self.filter_expenses)
        self.filter_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

        self.view_all_button = ttk.Button(self.window, text="View All", command=self.view_all_expenses)
        self.view_all_button.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

        separator = ttk.Separator(self.window, orient="horizontal")
        separator.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.dashboard_frame = ttk.LabelFrame(self.window, text="Dashboard")
        self.dashboard_frame.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

        self.total_expenses_label = ttk.Label(self.dashboard_frame, text="Total Expenses: $0.00")
        self.total_expenses_label.grid(row=0, column=0, padx=5, pady=5)
        self.total_income_label = ttk.Label(self.dashboard_frame, text="Total Income: $0.00")
        self.total_income_label.grid(row=0, column=1, padx=5, pady=5)
        self.total_savings_label = ttk.Label(self.dashboard_frame, text="Total Savings: $0.00")
        self.total_savings_label.grid(row=0, column=2, padx=5, pady=5)

        self.tips_frame = ttk.LabelFrame(self.window, text="Finance Tips")
        self.tips_frame.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tips_text = tk.Text(self.tips_frame, height=5, width=50, wrap="word")
        self.tips_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.refresh_button = ttk.Button(self.window, text="Refresh", command=self.clear_all_fields)
        self.refresh_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

    def add_expense(self):
        # Retrieve expense, amount, category, income, and savings from the entry fields
        expense = self.expense_entry.get()
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        income = float(self.income_entry.get())
        savings = float(self.savings_entry.get())

        # Add the expense, income, and savings using the Tracker class
        self.tracker.add_expense(expense, amount, category, income, savings)

        # Refresh the expense list and clear the entry fields
        self.refresh_expense_list()
        self.clear_entry_fields()

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            expense_info = self.expense_listbox.get(selected_index)
            expense_id = int(expense_info.split(":")[0])

            # Delete the expense using the Tracker class
            self.tracker.delete_expense(expense_id)

            # Refresh the expense list
            self.refresh_expense_list()
        else:
            messagebox.showinfo("Delete Expense", "Please select an expense to delete.")

    def filter_expenses(self):
        filter_value = self.filter_entry.get()
        if filter_value:
            try:
                month, year = map(int, filter_value.split("/"))
                expenses = self.tracker.get_expenses_by_month_year(month, year)
                self.display_expenses(expenses)
            except ValueError:
                messagebox.showinfo("Filter Expenses", "Invalid filter value. Please provide month/year (e.g., 5/2023).")
        else:
            messagebox.showinfo("Filter Expenses", "Please provide a filter value.")

    def view_all_expenses(self):
        # Refresh the expense list to display all expenses
        self.refresh_expense_list()

    def refresh_expense_list(self):
        # Clear the expense listbox
        self.expense_listbox.delete(0, tk.END)

        expenses = self.tracker.get_expenses()
        self.display_expenses(expenses)

        # Calculate and update the dashboard labels
        total_expenses = sum(expense[2] for expense in expenses)
        total_income = sum(expense[4] for expense in expenses)
        total_savings = sum(expense[5] for expense in expenses)

        self.total_expenses_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
        self.total_income_label.config(text=f"Total Income: ${total_income:.2f}")
        self.total_savings_label.config(text=f"Total Savings: ${total_savings:.2f}")

        self.load_finance_tips()  # Reload finance tips after updating expenses

    def display_expenses(self, transactions):
        for transaction in transactions:
            expense_id, expense, amount, category, income, savings, month, year = transaction
            expense_info = f"{expense_id}: {expense} - Rs {amount} - {category} ({month}/{year}) - Income: Rs {income} - Savings: Rs {savings}"
            self.expense_listbox.insert(tk.END, expense_info)

    def clear_entry_fields(self):
        self.expense_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.filter_entry.delete(0, tk.END)
        self.income_entry.delete(0, tk.END)
        self.savings_entry.delete(0, tk.END)

    def clear_all_fields(self):
        self.clear_entry_fields()
        self.expense_listbox.delete(0, tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run() 