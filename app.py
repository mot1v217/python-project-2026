from flask import Flask, render_template
import pandas as pd
import json


app = Flask(__name__)

def load_reports_with_statuses():
    """Читает CSV и JSON, объединяет по статусу, возвращает DataFrame."""
    reports = pd.read_csv("data/reports.csv")
    
    with open("data/statuses.json", encoding="utf-8") as f:
        statuses = json.load(f)
    statuses_df = pd.DataFrame(statuses)
    statuses_df = statuses_df.rename(columns={"id": "status_id"})
    
    merged = reports.merge(statuses_df, left_on="status", right_on="status_id", how="left")
    merged["status_name"] = merged["status_name"].fillna("неизвестно")
    return merged

@app.route("/")
def index():
    reports = load_reports_with_statuses()
    return render_template("index.html", reports=reports.to_dict("records"))

@app.route("/report/<int:report_id>")
def report_detail(report_id):
    reports = load_reports_with_statuses()
    report = reports[reports["id"] == report_id].iloc[0]
    return render_template("report.html", report=report.to_dict())

if __name__ == "__main__":
    app.run(debug=True)