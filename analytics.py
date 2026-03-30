import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "sublet_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"expenses": [], "budget": {}}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def get_monthly_summary(month=None, year=None):
    """Calculates totals per category and compares against budget."""
    data = load_data()
    expenses = data.get("expenses", [])
    budget = data.get("budget", {})

    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year

    monthly_totals = defaultdict(float)
    for exp in expenses:
        date = datetime.strptime(exp['date'], '%Y-%m-%d')
        if date.month == month and date.year == year:
            monthly_totals[exp['category']] += exp['amount']

    return monthly_totals, budget

def print_analytics_report():
    """Generates and prints a formatted terminal report."""
    totals, budget = get_monthly_summary()
    
    print(f"\n--- Monthly Analytics Report ({datetime.now().strftime('%B %Y')}) ---")
    print(f"{'Category':<15} | {'Spent':<10} | {'Budget':<10} | {'Status'}")
    print("-" * 50)
    
    total_spent = 0
    total_budget = 0
    
    categories = set(list(totals.keys()) + list(budget.keys()))
    
    for cat in sorted(categories):
        spent = totals.get(cat, 0.0)
        limit = budget.get(cat, 0.0)
        total_spent += spent
        total_budget += limit
        
        status = "OK"
        if limit > 0 and spent > limit:
            status = "!! OVER !!"
            
        print(f"{cat.capitalize():<15} | ${spent:<9.2f} | ${limit:<9.2f} | {status}")
        
    print("-" * 50)
    print(f"{'TOTAL':<15} | ${total_spent:<9.2f} | ${total_budget:<9.2f}")
    
    if total_budget > 0 and total_spent > total_budget:
        print("\nALERT: You have exceeded your total monthly budget!")
    else:
        print("\nStatus: Within budget.")

def set_monthly_budget(category, amount):
    """Updates the budget for a specific category."""
    data = load_data()
    data.setdefault("budget", {})
    data["budget"][category] = float(amount)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Budget for {category} set to ${amount:.2f}")