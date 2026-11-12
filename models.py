from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class District(db.Model):
    '''Модель округов и их id'''
    __tablename__ = "districts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Status(db.Model):
    '''Модель статусов и их id'''
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(50), nullable=False)

class Report(db.Model):
    '''Модель обращений'''
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey("districts.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"))
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)
    photo_path = db.Column(db.String(255))
    date = db.Column(db.Date)
    resolved_date = db.Column(db.Date, nullable=True)
    comment = db.Column(db.Text)

    district = db.relationship("District", backref="reports")
    status = db.relationship("Status", backref="reports")