from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    data=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))


class Requests(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    userRequest=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    status=db.Column(db.String(20), default="active")

class Log(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email=db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role=db.Column(db.String(10))

class Activity(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    activity=db.Column(db.String(10000))
    date=db.Column(db.String(120))

class Family(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    residentId=db.Column(db.Integer, db.ForeignKey('user.id'))
    email=db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    contactNo = db.Column(db.String(10))
    resident_name=db.Column(db.String(150))
    role=db.Column(db.String(10))

class Staff(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    contactNo = db.Column(db.String(10))
    residents=db.relationship('User')
    role=db.Column(db.String(10))

class Admin(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    contactNo = db.Column(db.String(10))
    role=db.Column(db.String(10))


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    staffId=db.Column(db.Integer, db.ForeignKey('staff.id'))
    name = db.Column(db.String(150))
    age=db.Column(db.String(5))
    contactNo = db.Column(db.String(10))
    role=db.Column(db.String(10))
    notes=db.relationship('Note')
    requests=db.relationship('Requests')
    family=db.relationship('Family')
    activity=db.relationship('Activity')