# expense.py
from datetime import datetime

class Expense:
    def __init__(self, date, category, amount, description=""):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "category": self.category,
            "amount": float(self.amount),
            "description": self.description
        }
