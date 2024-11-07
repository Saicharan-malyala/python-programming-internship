import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transportation", "Entertainment", "Other"]

# Functions
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file)

def add_expense():
    try:
        amount = float(amount_entry.get())
        description = description_entry.get()
        category = category_var.get()
        month = month_entry.get()
        year = year_entry.get()

        if not all([description, category, month, year]):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return
        
        if not (month.isdigit() and year.isdigit()):
            messagebox.showerror("Invalid Input", "Please enter numeric values for month and year.")
            return
        
        date = f"{year}-{month.zfill(2)}"

        expense = {
            "amount": amount,
            "description": description,
            "category": category,
            "date": date
        }
        expenses.append(expense)
        save_data(expenses)
        
        # Clear input fields
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        category_var.set(CATEGORIES[0])
        month_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Expense added successfully!")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")

def view_summary():
    total_spent = sum(expense["amount"] for expense in expenses)
    summary_text = f"Total Expenses: ${total_spent:.2f}\n\nExpenses by Category:\n"
    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        category_totals[category] = category_totals.get(category, 0) + expense["amount"]
    
    for category, amount in category_totals.items():
        summary_text += f"{category}: ${amount:.2f}\n"
    
    summary_tab_summary_label.config(text=summary_text)
    
    # Generate Pie Chart
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Category-wise Expenses')
    chart = FigureCanvasTkAgg(fig, master=summary_tab)
    chart.draw()
    chart.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def view_monthly_summary():
    month = month_summary_entry.get()
    year = year_summary_entry.get()
    
    if not (month.isdigit() and year.isdigit()):
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for month and year.")
        return
    
    monthly_expenses = [expense for expense in expenses if expense["date"].startswith(f"{year}-{month.zfill(2)}")]
    
    if not monthly_expenses:
        monthly_summary_tab_summary_label.config(text="No expenses found for this month.")
        return
    
    monthly_total = sum(expense["amount"] for expense in monthly_expenses)
    summary_text = f"Total Expenses for {year}-{month.zfill(2)}: ${monthly_total:.2f}\n\nExpenses by Category:\n"
    
    category_totals = {}
    for expense in monthly_expenses:
        category = expense["category"]
        category_totals[category] = category_totals.get(category, 0) + expense["amount"]
    
    for category, amount in category_totals.items():
        summary_text += f"{category}: ${amount:.2f}\n"
    
    monthly_summary_tab_summary_label.config(text=summary_text)
    
    # Generate Pie Chart for Monthly Summary
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title(f'Monthly Expenses for {year}-{month.zfill(2)}')
    chart = FigureCanvasTkAgg(fig, master=monthly_summary_tab)
    chart.draw()
    chart.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Expense Tracker")

# Load existing data or initialize an empty list
expenses = load_data()

# Create Notebook (for tabs)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Tab 1: Add Expense
add_expense_tab = ttk.Frame(notebook)
notebook.add(add_expense_tab, text='Add Expense')

tk.Label(add_expense_tab, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
amount_entry = tk.Entry(add_expense_tab)
amount_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(add_expense_tab, text="Description:").grid(row=1, column=0, padx=10, pady=5)
description_entry = tk.Entry(add_expense_tab)
description_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(add_expense_tab, text="Category:").grid(row=2, column=0, padx=10, pady=5)
category_var = tk.StringVar(add_expense_tab)
category_var.set(CATEGORIES[0])
category_menu = tk.OptionMenu(add_expense_tab, category_var, *CATEGORIES)
category_menu.grid(row=2, column=1, padx=10, pady=5)

tk.Label(add_expense_tab, text="Month (MM):").grid(row=3, column=0, padx=10, pady=5)
month_entry = tk.Entry(add_expense_tab)
month_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(add_expense_tab, text="Year (YYYY):").grid(row=4, column=0, padx=10, pady=5)
year_entry = tk.Entry(add_expense_tab)
year_entry.grid(row=4, column=1, padx=10, pady=5)

add_expense_button = tk.Button(add_expense_tab, text="Add Expense", command=add_expense)
add_expense_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Tab 2: Summary
summary_tab = ttk.Frame(notebook)
notebook.add(summary_tab, text='View Summary')

summary_button = tk.Button(summary_tab, text="View Summary", command=view_summary)
summary_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

summary_tab_summary_label = tk.Label(summary_tab, text="", justify="left", anchor="w")
summary_tab_summary_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Tab 3: Monthly Summary
monthly_summary_tab = ttk.Frame(notebook)
notebook.add(monthly_summary_tab, text='Monthly Summary')

tk.Label(monthly_summary_tab, text="Month (MM):").grid(row=0, column=0, padx=10, pady=5)
month_summary_entry = tk.Entry(monthly_summary_tab)
month_summary_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(monthly_summary_tab, text="Year (YYYY):").grid(row=1, column=0, padx=10, pady=5)
year_summary_entry = tk.Entry(monthly_summary_tab)
year_summary_entry.grid(row=1, column=1, padx=10, pady=5)

monthly_summary_button = tk.Button(monthly_summary_tab, text="View Monthly Summary", command=view_monthly_summary)
monthly_summary_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

monthly_summary_tab_summary_label = tk.Label(monthly_summary_tab, text="", justify="left", anchor="w")
monthly_summary_tab_summary_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Run the main loop
root.mainloop()
