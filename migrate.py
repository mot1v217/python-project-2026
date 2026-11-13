import json
from datetime import date
from app import app
from models import db, District, Status, Report
import shutil
import os

with app.app_context():
    db.drop_all()
    if os.path.exists("static/uploads"):
        shutil.rmtree("static/uploads")
    os.makedirs("static/uploads", exist_ok=True)
    db.create_all()
    print("Таблицы созданы")

    with open("data/districts.json", encoding="utf-8") as f:
        for d in json.load(f):
            db.session.add(District(id=d["id"], name=d["name"]))
    print("Округа загружены")

    with open("data/statuses.json", encoding="utf-8") as f:
        for s in json.load(f):
            db.session.add(Status(id=s["id"], status_name=s["status_name"]))
    print("Статусы загружены")

    db.session.commit()
    print("БД создана")