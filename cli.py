import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any

DATA_FILE = "sublet_data.json"
CATEGORIES = ["rent", "electric", "water", "internet", "other"]

def load_data() -> Dict[str, Any]:
    if not os.path.exists(DATA_FILE):
        return {"budget": 0.0, "expenses": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data: Dict[str, Any]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense(amount: float, category: str, description: str):
    data = load_data()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "category": category,
        "description": description
    }
    data["expenses"].append(entry)
    save_data(data)
    print(f"Successfully logged {category}: ${amount:.2f}")

def set_budget(amount: float):
    data = load_data()
    data["budget"] = amount
    save_data(data)
    print(f"Budget set to ${amount:.2f}")

def generate_report():
    data = load_data()
    current_month = datetime.now().strftime("%Y-%m")
    monthly_expenses = [
        e for e in data["expenses"] 
        if e["date"].startswith(current_month)
    ]
    total_spent = sum(e["amount"] for e in monthly_expenses)
    
    print(f"\n--- Report for {current_month} ---")
    for e in monthly_expenses:
        print(f"{e['date']} | {e['category'].upper():<10} | ${e['amount']:>8.2f} | {e['description']}")
    
    print("-" * 30)
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Budget:      ${data['budget']:.2f}")
    
    if data["budget"] > 0:
        diff = data["budget"] - total_spent
        if diff < 0:
            print(f"ALERT: You are over budget by ${abs(diff):.2f}!")
        else:
            print(f"Remaining:   ${diff:.2f}")

def main():
    parser = argparse.ArgumentParser(description="SubletScript: Manage your living expenses.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Log an expense")
    add_parser.add_argument("amount", type=float)
    add_parser.add_argument("category", choices=CATEGORIES)
    add_parser.add_argument("description", type=str)

    budget_parser = subparsers.add_parser("budget", help="Set monthly budget")
    budget_parser.add_argument("amount", type=float)

    subparsers.add_parser("report", help="View monthly summary")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.description)
    elif args.command == "budget":
        set_budget(args.amount)
    elif args.command == "report":
        generate_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()