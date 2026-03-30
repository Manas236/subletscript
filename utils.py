import json
import os
from datetime import datetime

DATA_FILE = "sublet_data.json"

def load_data():
    """Loads the JSON data file or returns a default structure."""
    if not os.path.exists(DATA_FILE):
        return {"expenses": [], "budget": 0.0}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"expenses": [], "budget": 0.0}

def save_data(data):
    """Saves the data dictionary to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_category(category):
    """Validates if the provided category is allowed."""
    valid_categories = ["water", "electric", "internet", "rent", "other"]
    return category.lower() in valid_categories

def get_monthly_total(expenses, month, year):
    """Calculates total spending for a specific month and year."""
    total = 0.0
    for exp in expenses:
        date = datetime.strptime(exp["date"], "%Y-%m-%d")
        if date.month == month and date.year == year:
            total += exp["amount"]
    return total

def format_currency(amount):
    """Returns a string formatted as currency."""
    return f"${amount:,.2f}"

def get_current_month_year():
    """Returns current month and year as integers."""
    now = datetime.now()
    return now.month, now.year

def print_report(expenses, budget, month, year):
    """Generates a summary report for the terminal."""
    total = get_monthly_total(expenses, month, year)
    print(f"\n--- Report for {month}/{year} ---")
    print(f"Total Spent: {format_currency(total)}")
    print(f"Budget:      {format_currency(budget)}")
    
    if budget > 0:
        diff = budget - total
        status = "UNDER" if diff >= 0 else "OVER"
        print(f"Status:      {status} budget by {format_currency(abs(diff))}")
        if diff < 0:
            print("ALERT: You have exceeded your monthly budget!")
    print("----------------------------\n")