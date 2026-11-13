from flask import Flask, render_template
import csv
from io import StringIO, BytesIO
from flask import send_file
import os
import uuid
from datetime import date
from flask import request, redirect, url_for
from geocoder import get_coordinates

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from models import db, Report, District
db.init_app(app)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route("/report/add", methods=["GET"])
def add_report_form():
    districts = District.query.all()
    return render_template("add_report.html", districts=districts)


@app.route("/report/add", methods=["POST"])
def add_report_submit():
    address = request.form.get("address")
    district_id = request.form.get("district_id")
    comment = request.form.get("comment")

    file = request.files.get("photo")

    if not file or file.filename == "":
        return "Ошибка: фото обязательно", 400
    if not allowed_file(file.filename):
        return "Ошибка: только jpg/png", 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    lat, lon = get_coordinates(address)
    print(f"DEBUG: Адрес {address} -> lat={lat}, lon={lon}")

    new_report = Report(
        address=address,
        district_id=int(district_id),
        status_id=0,  # 0 = "новое"
        photo_path=f"uploads/{filename}",
        date=date.today(),
        comment=comment,
        lat=lat,
        lon=lon,
    )
    db.session.add(new_report)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
