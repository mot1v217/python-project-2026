import json
from datetime import date
from app import app
from models import db, District, Status, Report

with app.app_context():
    db.drop_all()
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

    db.session.add(Report(
        address="Карла Маркса, 9А",
        district_id=1,
        status_id=2,
        photo_path="uploads/Photo1.jfif",
        date=date(2024, 9, 15),
        resolved_date=date(2024, 9, 20),
        comment="Реклама слева от входа",
    ))
    db.session.add(Report(
        address="Ленина, 22",
        district_id=1,
        status_id=1,
        photo_path="uploads/Photo2.jfif",
        date=date(2024, 9, 18),
        comment="Между окнами",
    ))
    db.session.add(Report(
        address="Свердлова, 15",
        district_id=1,
        status_id=0,
        photo_path="uploads/Photo3.jfif",
        date=date(2024, 9, 20),
        comment="На колонне",
    ))
    print("Сообщения добавлены")

    db.session.commit()
    print("БД создана и заполнена")