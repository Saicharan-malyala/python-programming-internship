# Importing necessary libraries
import tkinter as tk  # For GUI application creation
from tkinter import ttk, messagebox # For tabbed interface and messageboxes
import json # For reading and writing JSON data (used for saving expenses)
from datetime import datetime # For handling date and time
import os # For checking file existence
import matplotlib.pyplot as plt # For plotting graphs (e.g., Pie chart)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # For embedding Matplotlib figures into Tkinter


# Constants (Fixed values used throughout the application)
DATA_FILE = "expenses.json" # The name of the file where expenses are saved
CATEGORIES = ["Food", "Transportation", "Entertainment", "Other"]  # List of categories for expenses

# Functions (Each function is responsible for specific tasks)
def load_data():
    """Loads the expense data from the JSON file if it exists. If the file doesn't exist, returns an empty list."""
    if os.path.exists(DATA_FILE): # Checks if the expenses file exists
        with open(DATA_FILE, 'r') as file: # Opens the file in read mode
            return json.load(file) # Loads and returns the data as a list
    return [] # If the file doesn't exist, returns an empty list

def save_data(expenses):
    """Saves the given list of expenses into a JSON file."""
    with open(DATA_FILE, 'w') as file: # Opens the file in write mode
        json.dump(expenses, file)  # Dumps the expenses list as JSON into the file

def add_expense():
    """Handles adding a new expense by reading input fields and saving the new expense."""
    try: # Retrieves the input values from the user interface
        amount = float(amount_entry.get()) # Converts the entered amount to a float
        description = description_entry.get()# Gets the description of the expense
        category = category_var.get() # Gets the selected category
        month = month_entry.get()# Gets the month value
        year = year_entry.get()# Gets the year value
        # Checks if all fields are filled
        if not all([description, category, month, year]):
            messagebox.showwarning("Input Error", "Please fill all fields.") # Shows a warning if any field is empty
            return
        # Validates the month and year as numeric values
        if not (month.isdigit() and year.isdigit()):
            messagebox.showerror("Invalid Input", "Please enter numeric values for month and year.") # Error message for invalid input
            return
         # Creates a date string in the format "YYYY-MM"
        date = f"{year}-{month.zfill(2)}" # `zfill(2)` ensures month is always 2 digits
        # Creates a dictionary to store the expense details
        expense = {
            "amount": amount,
            "description": description,
            "category": category,
            "date": date
        }
        expenses.append(expense)  # Adds the new expense to the list of expenses
        save_data(expenses) # Saves the updated list of expenses to the JSON file
        
        # Clear input fields after saving the expense
        amount_entry.delete(0, tk.END) # Clears the amount field
        description_entry.delete(0, tk.END) # Clears the description field
        category_var.set(CATEGORIES[0]) # Resets category selection to the first option
        month_entry.delete(0, tk.END) # Clears the month field
        year_entry.delete(0, tk.END) # Clears the year field
        # Shows a success message
        messagebox.showinfo("Success", "Expense added successfully!")
    except ValueError:
        # Error handling for invalid amount input
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")

def view_summary():
    """Displays a summary of all expenses, including the total and category-wise breakdown"""
    total_spent = sum(expense["amount"] for expense in expenses)  # Calculates the total expenses
    summary_text = f"Total Expenses: ${total_spent:.2f}\n\nExpenses by Category:\n"
    # Creates a dictionary to store total amounts for each category
    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        category_totals[category] = category_totals.get(category, 0) + expense["amount"]
        # Adds category-wise breakdown to the summary text
    
    for category, amount in category_totals.items():
        summary_text += f"{category}: ${amount:.2f}\n"
    # Updates the summary label with the calculated text
    summary_tab_summary_label.config(text=summary_text)
    
    # Generate Pie Chart
    categories = list(category_totals.keys()) # Categories list
    amounts = list(category_totals.values()) # Corresponding amounts
    fig, ax = plt.subplots(figsize=(6, 5), dpi=100) # Creates a figure and axis for the pie chart
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90) # Plots the pie chart
    ax.axis('equal') # Ensures the pie chart is circular
    ax.set_title('Category-wise Expenses') # Sets the title for the chart
    chart = FigureCanvasTkAgg(fig, master=summary_tab) # Converts the Matplotlib chart to a Tkinter widget
    chart.draw() # Draws the chart
    chart.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=10, pady=10) # Places the chart in the UI

def view_monthly_summary():
    month = month_summary_entry.get() # Gets the entered month
    year = year_summary_entry.get()  # Gets the entered year
    
    if not (month.isdigit() and year.isdigit()):
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for month and year.")
        return
     # Filters the expenses to include only those that match the entered month and year
    monthly_expenses = [expense for expense in expenses if expense["date"].startswith(f"{year}-{month.zfill(2)}")]
    
    if not monthly_expenses: # If no expenses match, shows a message
        monthly_summary_tab_summary_label.config(text="No expenses found for this month.")
        return
     # Calculates the total and category-wise expenses for the month
    monthly_total = sum(expense["amount"] for expense in monthly_expenses)
    summary_text = f"Total Expenses for {year}-{month.zfill(2)}: ${monthly_total:.2f}\n\nExpenses by Category:\n"
    
    category_totals = {}
    for expense in monthly_expenses:
        category = expense["category"]
        category_totals[category] = category_totals.get(category, 0) + expense["amount"]
    # Adds category-wise breakdown to the summary text
    for category, amount in category_totals.items():
        summary_text += f"{category}: ${amount:.2f}\n"
    # Updates the monthly summary label with the calculated text
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
root.title("Expense Tracker") # Sets the title of the window

# Load existing data or initialize an empty list
expenses = load_data() # Loads the expenses from the JSON file

# Create Notebook (for tabs)
notebook = ttk.Notebook(root) # Creates a tabbed interface
notebook.pack(pady=10, expand=True) # Adds the notebook to the window

# Tab 1: Add Expense
add_expense_tab = ttk.Frame(notebook)  # Creates a frame for the "Add Expense" tab
notebook.add(add_expense_tab, text='Add Expense') # Adds the tab to the notebook

# Creating input fields and labels for the "Add Expense" tab
tk.Label(add_expense_tab, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
amount_entry = tk.Entry(add_expense_tab) # Entry widget for amount
amount_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(add_expense_tab, text="Description:").grid(row=1, column=0, padx=10, pady=5)
description_entry = tk.Entry(add_expense_tab) # Entry widget for description
description_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(add_expense_tab, text="Category:").grid(row=2, column=0, padx=10, pady=5)
category_var = tk.StringVar(add_expense_tab) # Variable for category selection
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
