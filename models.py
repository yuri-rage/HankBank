from flask_login import UserMixin
from app import db
from enum import Enum


class Permissions(Enum):
    admin = 0
    parent = 1
    child = 2


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    permission = db.Column(db.Enum(Permissions))
    transactions = db.relationship('Transaction', backref='user', lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    memo = db.Column(db.String(1000))
    approved = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
