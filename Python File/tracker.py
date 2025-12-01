# tracker.py
import os
import pandas as pd
from expense import Expense

class ExpenseTracker:

    def __init__(self, path="data/expenses.csv"):
        self.path = path
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.path):
            df = pd.DataFrame(columns=["date", "category", "amount", "description"])
            df.to_csv(self.path, index=False)

    def read_expenses(self):
        try:
            df = pd.read_csv(self.path, parse_dates=["date"])
            return df
        except FileNotFoundError:
            print("Error: CSV file missing.")
            return pd.DataFrame()

    def add_expense(self, expense: Expense):
        try:
            df = self.read_expenses()
            df.loc[len(df)] = expense.to_dict()
            df.to_csv(self.path, index=False)
        except Exception as e:
            print("Error saving expense:", e)

    def filter_category(self, category):
        df = self.read_expenses()
        return df[df["category"].str.lower() == category.lower()]

    def filter_date(self, start, end):
        df = self.read_expenses()
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        return df[(df["date"] >= start) & (df["date"] <= end)]

    def search(self, text):
        df = self.read_expenses()
        return df[df.apply(lambda r: text.lower() in str(r).lower(), axis=1)]
