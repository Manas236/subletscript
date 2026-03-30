import json
import os
from typing import List, Dict, Any, Optional

class StorageManager:
    def __init__(self, filepath: str = "sublet_data.json"):
        self.filepath = filepath
        self._initialize_file()

    def _initialize_file(self):
        """Creates the JSON file if it does not exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({"expenses": [], "budget": 0.0}, f, indent=4)

    def _read_data(self) -> Dict[str, Any]:
        """Reads the entire storage file."""
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write_data(self, data: Dict[str, Any]):
        """Writes data to the JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def add_expense(self, category: str, amount: float, date: str, note: str = ""):
        """Appends a new expense to the data file."""
        data = self._read_data()
        new_expense = {
            "category": category.lower(),
            "amount": amount,
            "date": date,
            "note": note
        }
        data["expenses"].append(new_expense)
        self._write_data(data)

    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """Returns a list of all logged expenses."""
        return self._read_data().get("expenses", [])

    def set_budget(self, amount: float):
        """Updates the monthly budget limit."""
        data = self._read_data()
        data["budget"] = amount
        self._write_data(data)

    def get_budget(self) -> float:
        """Retrieves the current budget."""
        return self._read_data().get("budget", 0.0)

    def clear_all_data(self):
        """Resets the storage file."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        self._initialize_file()

    def get_expenses_by_month(self, month_year: str) -> List[Dict[str, Any]]:
        """
        Filters expenses by a specific month (format: YYYY-MM).
        Assumes date format YYYY-MM-DD.
        """
        all_expenses = self.get_all_expenses()
        return [e for e in all_expenses if e['date'].startswith(month_year)]