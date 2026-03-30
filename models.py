import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Expense:
    id: int
    category: str
    amount: float
    date: str
    description: str

    def to_dict(self):
        return asdict(self)

class ExpenseManager:
    def __init__(self, storage_path: str = "sublet_data.json"):
        self.storage_path = storage_path
        self.expenses: List[Expense] = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                try:
                    data = json.load(f)
                    self.expenses = [Expense(**item) for item in data]
                except (json.JSONDecodeError, TypeError):
                    self.expenses = []

    def save_data(self):
        with open(self.storage_path, 'w') as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=4)

    def add_expense(self, category: str, amount: float, description: str) -> int:
        new_id = max([e.id for e in self.expenses], default=0) + 1
        new_expense = Expense(
            id=new_id,
            category=category.lower(),
            amount=amount,
            date=datetime.now().strftime("%Y-%m-%d"),
            description=description
        )
        self.expenses.append(new_expense)
        self.save_data()
        return new_id

    def get_monthly_expenses(self, year: int, month: int) -> List[Expense]:
        target_prefix = f"{year}-{month:02d}"
        return [e for e in self.expenses if e.date.startswith(target_prefix)]

    def get_total_by_category(self, year: int, month: int) -> dict:
        monthly = self.get_monthly_expenses(year, month)
        summary = {}
        for expense in monthly:
            summary[expense.category] = summary.get(expense.category, 0) + expense.amount
        return summary

    def check_budget(self, year: int, month: int, budget: float) -> dict:
        monthly = self.get_monthly_expenses(year, month)
        total = sum(e.amount for e in monthly)
        return {
            "total": total,
            "budget": budget,
            "remaining": budget - total,
            "is_over": total > budget
        }

    def delete_expense(self, expense_id: int) -> bool:
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        if len(self.expenses) < original_count:
            self.save_data()
            return True
        return False