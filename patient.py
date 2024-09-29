from . import db
from flask_login import UserMixin

class Patient(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))