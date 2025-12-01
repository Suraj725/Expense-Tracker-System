# report.py
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from sklearn.linear_model import LinearRegression

# reportlab font registration (kept in case you add fonts later)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Attempt to register a Devanagari-capable TTF from project root (optional)
DEVANAGARI_TTF = None
DEVANAGARI_FONT_NAME = None
for candidate in ("NotoSansDevanagari-Regular.ttf", "DejaVuSans.ttf", "NotoSans-Regular.ttf"):
    if os.path.exists(candidate):
        try:
            font_name = os.path.splitext(os.path.basename(candidate))[0]
            pdfmetrics.registerFont(TTFont(font_name, candidate))
            DEVANAGARI_TTF = candidate
            DEVANAGARI_FONT_NAME = font_name
            break
        except Exception:
            DEVANAGARI_TTF = None
            DEVANAGARI_FONT_NAME = None
            break

# Fallback font name for Latin text (page numbers, headings)
FALLBACK_FONT = "Helvetica"

class ReportGenerator:

    def __init__(self, path="data/expenses.csv"):
        self.path = path
        os.makedirs("reports", exist_ok=True)

    # -------------------------
    # Load & Clean Data
    # -------------------------
    def load_data(self):
        try:
            df = pd.read_csv(self.path)
        except FileNotFoundError:
            print("ERROR: expenses.csv not found at", self.path)
            return pd.DataFrame()

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        # Ensure description exists
        if "description" not in df.columns:
            df["description"] = ""
        return df

    # -------------------------
    # Monthly Summary
    # -------------------------
    def monthly_summary(self):
        df = self.load_data()
        if df.empty:
            return pd.DataFrame()
        df["month"] = df["date"].dt.to_period("M").astype(str)
        summary = df.groupby("month")["amount"].sum().reset_index()
        return summary

    # -------------------------
    # Excel export
    # -------------------------
    def export_excel(self):
        summary = self.monthly_summary()
        if summary.empty:
            print("No data to export.")
            return None
        save_path = "reports/monthly_summary.xlsx"
        summary.to_excel(save_path, index=False)
        return save_path

    # -------------------------
    # Plotting helpers
    # -------------------------
    def plot_trend(self):
        summary = self.monthly_summary()
        if summary.empty:
            print("No data available to plot.")
            return None
        plt.figure(figsize=(10, 5))
        plt.plot(summary["month"], summary["amount"], marker="o")
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Amount (₹)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        save_path = "reports/spending_trend.png"
        plt.savefig(save_path)
        plt.close()
        return save_path

    def plot_category_pie(self):
        df = self.load_data()
        if df.empty:
            print("No data available for pie chart.")
            return None
        category_sum = df.groupby("category")["amount"].sum()
        plt.figure(figsize=(8, 8))
        plt.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%")
        plt.title("Category-wise Spending Distribution")
        plt.tight_layout()
        save_path = "reports/category_pie_chart.png"
        plt.savefig(save_path)
        plt.close()
        return save_path

    def plot_monthly_bar(self):
        summary = self.monthly_summary()
        if summary.empty:
            print("No data available for bar chart.")
            return None
        plt.figure(figsize=(10, 5))
        plt.bar(summary["month"], summary["amount"])
        plt.title("Monthly Spending Bar Chart")
        plt.xlabel("Month")
        plt.ylabel("Total Amount (₹)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        save_path = "reports/monthly_bar_chart.png"
        plt.savefig(save_path)
        plt.close()
        return save_path

    def plot_top_expenses(self):
        df = self.load_data()
        if df.empty:
            return None
        top10 = df.sort_values(by="amount", ascending=False).head(10)
        # shorten descriptions to avoid extremely long tick labels
        labels = [str(d)[:30] for d in top10["description"].astype(str)]
        plt.figure(figsize=(10, 5))
        plt.bar(labels, top10["amount"])
        plt.title("Top 10 Highest Expenses")
        plt.xlabel("Expense Description")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=60, ha="right")
        plt.tight_layout()
        save_path = "reports/top_10_expenses.png"
        plt.savefig(save_path)
        plt.close()
        return save_path

    # -------------------------
    # Prediction
    # -------------------------
    def predict_next_month(self):
        summary = self.monthly_summary()
        if len(summary) < 2:
            print("Need at least 2 months of data for prediction.")
            return None
        X = np.arange(len(summary)).reshape(-1, 1)
        y = summary["amount"].values
        model = LinearRegression()
        model.fit(X, y)
        next_index = [[len(summary)]]
        next_month_prediction = model.predict(next_index)[0]
        return round(float(next_month_prediction), 2)

    # -------------------------
    # Project info helpers
    # -------------------------
    def _load_project_info(self, project_info):
        if project_info and isinstance(project_info, dict):
            return project_info
        info_path = "project_info.json"
        if os.path.exists(info_path):
            try:
                with open(info_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print("Warning: failed to read project_info.json:", e)
        # fallback defaults
        return {
            "project_title": "Smart Expense Tracker",
            "project_name": "Smart Expense Tracker System",
            "course": "",
            "institute": "",
            "supervisor": "",
            "semester": "",
            "generated_by": "Smart Expense Tracker System",
            "team": []
        }

    # -------------------------
    # Footer helper (page number only)
    # -------------------------
    def _add_page_number(self, canvas_obj, doc_width, doc_height, page_num):
        """
        Draw footer: right = page number.
        """
        try:
            canvas_obj.setFont(FALLBACK_FONT, 9)
        except Exception:
            canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(colors.grey)
        canvas_obj.drawRightString(doc_width - 40, 30, f"Page {page_num}")
        canvas_obj.setFillColor(colors.black)

    # -------------------------
    # PDF Generation (group-ready, paginated table)
    # -------------------------
    def generate_pdf_report(self, project_info=None):
        df = self.load_data()
        summary = self.monthly_summary()
        info = self._load_project_info(project_info)

        pdf_path = "reports/Full_Expense_Report.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        styles = getSampleStyleSheet()

        page_num = 1

        # --- Cover page ---
        # optional logo
        logo_path = "logo.png"
        if os.path.exists(logo_path):
            try:
                c.drawImage(logo_path, width - 140, height - 130, width=100, height=100, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass

        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 80, info.get("project_title", "Smart Expense Tracker"))

        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 110, info.get("project_name", info.get("project_title", "")))
        c.drawCentredString(width / 2, height - 130, info.get("course", ""))
        c.drawCentredString(width / 2, height - 150, info.get("institute", ""))
        c.drawCentredString(width / 2, height - 170, f"Semester: {info.get('semester', '')}")

        c.setFont("Helvetica", 11)
        c.drawString(80, height - 200, f"Supervisor: {info.get('supervisor', '')}")
        c.drawString(80, height - 220, f"Generated by: {info.get('generated_by', '')}")
        c.drawString(80, height - 240, f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Team list — only names (roles removed)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(80, height - 270, "Team Members:")
        c.setFont("Helvetica", 11)
        y = height - 290
        for member in info.get("team", []):
            mname = member.get("name", "")
            # Print only the name — roles intentionally not shown
            c.drawString(90, y, f"- {mname}")
            y -= 16
            if y < 120:
                self._add_page_number(c, width, height, page_num)
                c.showPage()
                page_num += 1
                c.setFont("Helvetica", 11)
                y = height - 80

        # Footer and move on
        self._add_page_number(c, width, height, page_num)
        c.showPage()
        page_num += 1

        # --- Trend chart page ---
        trend_path = self.plot_trend()
        if trend_path:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(60, height - 60, "Monthly Spending Trend")
            try:
                c.drawImage(trend_path, 60, height - 380, width=480, height=300)
            except Exception:
                pass
            self._add_page_number(c, width, height, page_num)
            c.showPage()
            page_num += 1

        # --- Pie chart page ---
        pie_path = self.plot_category_pie()
        if pie_path:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(60, height - 60, "Category-wise Spending Distribution")
            try:
                c.drawImage(pie_path, 80, height - 460, width=400, height=400)
            except Exception:
                pass
            self._add_page_number(c, width, height, page_num)
            c.showPage()
            page_num += 1

        # --- Bar + Top10 page ---
        bar_path = self.plot_monthly_bar()
        top10_path = self.plot_top_expenses()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, height - 60, "Monthly Overview and Top Expenses")
        if bar_path:
            try:
                c.drawImage(bar_path, 60, height - 320, width=480, height=220)
            except Exception:
                pass
        if top10_path:
            try:
                c.drawImage(top10_path, 60, height - 640, width=480, height=260)
            except Exception:
                pass
        self._add_page_number(c, width, height, page_num)
        c.showPage()
        page_num += 1

        # --- Full expense table (paginated) ---
        if not df.empty:
            df_display = df.copy()
            df_display["date"] = df_display["date"].dt.strftime("%Y-%m-%d")
            # Build table rows (header + data)
            table_data = [["Date", "Category", "Amount (₹)", "Description"]]
            for _, r in df_display.iterrows():
                table_data.append([
                    r["date"],
                    str(r.get("category", "")),
                    f"{r.get('amount', 0):.2f}",
                    str(r.get("description", ""))
                ])

            # Break into chunks per page
            rows_per_page = 28  # adjust as needed
            start = 0
            total_rows = len(table_data)
            while start < total_rows:
                chunk = table_data[start:start + rows_per_page]
                t = Table(chunk, colWidths=[80, 120, 80, 260])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                ]))
                # Draw table
                w, h = t.wrapOn(c, width - 80, height - 120)
                t.drawOn(c, 40, height - 120 - h)
                self._add_page_number(c, width, height, page_num)
                start += rows_per_page
                c.showPage()
                page_num += 1

        # ensure file saved
        c.save()
        return pdf_path
