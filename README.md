# Expense-Tracker-System

Overview

Smart Expense Tracker is a Python-based personal finance management system that allows users to:
✔ Add & manage expenses
✔ Analyze spending with charts
✔ Generate monthly Excel reports
✔ Predict next month’s spending using Machine Learning
✔ Create professional multi-page PDF reports (with charts + full expense table + team details)
✔ Maintain clean data using CSV + Pandas
✔ Provide filters & search options


This project is built using the concepts of:
Functions
OOP (Object-Oriented Programming)
Exception Handling
File Handling
Pandas
Data Visualization (Matplotlib)
Machine Learning (Linear Regression)
PDF Report Generation (ReportLab)
📂 Project Folder Structure
SmartExpenseTracker/
│
├── main.py
├── expense.py
├── tracker.py
├── report.py
├── utils.py
│
├── project_info.json
│
├── data/
│   └── expenses.csv
│
└── reports/
    ├── monthly_summary.xlsx
    ├── spending_trend.png
    ├── category_pie_chart.png
    ├── monthly_bar_chart.png
    ├── top_10_expenses.png
    └── Full_Expense_Report.pdf




 Features
 1. Add Expense
Enter date, category, amount, and description → saved into CSV.
 2. View All Expenses
Displays your CSV in a clean table.
 3. Search Expense
Search any keyword across all columns.
 4. Filter by Category
View spending category-wise (Food, Rent, Shopping…).
 5. Filter by Date Range
Analyze any period: weekly/monthly/semester.
 6. Monthly Excel Report
Exports summary to:
reports/monthly_summary.xlsx
 7. Spending Trend Chart (Line Chart)
Shows monthly total spending changes.
 8. Category Pie Chart
Percentage-wise distribution of categories.
 9. Monthly Bar Chart
Visualize amount spent each month.
 10. Top 10 Highest Expenses Chart
Bar graph of the highest spending entries.
 11. AI-Powered Spending Prediction
Machine Learning (Linear Regression) predicts next month spending.
 12. Full PDF Report (Professional)
PDF includes:
Cover Page (Project Title + Team Members + Supervisor + Institute + Logo)
Spending Trend Chart
Category Pie Chart
Monthly Bar Chart
Top 10 Expenses Chart
Paginated Full Expense Table (with all descriptions)



 Installation & Setup
1️⃣ Clone or Download the Project
git clone <your-repo-url>
2️⃣ Install the required libraries
pip install pandas matplotlib scikit-learn reportlab
3️⃣ Create your project info file
Edit this file:
project_info.json
4️⃣ Add your expense dataset
Place expenses.csv inside:
/data/expenses.csv
5️⃣ Run the project
python3 main.py




Main Menu (CLI)
==== Smart Expense Tracker ====
1. Add Expense
2. View All Expenses
3. Search Expense
4. Filter By Category
5. Filter By Date Range
6. Generate Monthly Excel Report
7. Generate Spending Trend Plot
8. Generate Category-wise Pie Chart
9. Generate Monthly Bar Chart
10. Generate Top 10 Highest Expenses Chart
11. Predict Next Month Spending
12. Generate Full PDF Report
13. Edit Project Info
14. Exit



Technologies & Libraries Used
Component	        Technology
Core Language	    Python
Data Storage	    CSV, Pandas
Charts	            Matplotlib
PDF Reports	        ReportLab
Machine Learning	Scikit-Learn (Linear Regression)
CLI Interface	    Core Python Input/Output
