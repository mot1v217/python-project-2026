from flask import Flask, render_template
import csv
from io import StringIO, BytesIO
from flask import send_file

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from models import db, Report
db.init_app(app)

@app.route("/")
def index():
    reports = Report.query.all()
    return render_template("index.html", reports=reports)

@app.route("/report/<int:report_id>")
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template("report.html", report=report)

@app.route("/export/reports.csv")
def export_reports():
    reports = Report.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "address", "district", "status", "date", "resolved_date", "comment"])
    
    for r in reports:
        writer.writerow([
            r.id,
            r.address,
            r.district.name if r.district else "",
            r.status.status_name if r.status else "",
            r.date,
            r.resolved_date or "",
            r.comment or "",
        ])
    
    bytes_output = BytesIO(output.getvalue().encode("utf-8"))
    
    return send_file(
        bytes_output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="reports.csv",
    )

if __name__ == "__main__":
    app.run(debug=True)
