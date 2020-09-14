from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
import datetime

import click
from flask.cli import with_appcontext

@with_appcontext
def create_tables():
    db.create_all()

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    login_counter = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_premium = db.Column(db.Boolean, nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
						"first_name": self.first_name,
						"last_name": self.last_name,
            "email": self.email,
						"phone_number": self.phone_number,
            "password": self.password,
						"login_counter": self.login_counter,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S"),
						"is_admin": self.is_admin,
						"is_premium": self.is_premium,
						"email_confirmed": self.email_confirmed
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    monthly = db.Column(db.Boolean, nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    catagory = db.Column(db.String(120), nullable=False)
    sub_catagory = db.Column(db.String(120), nullable=True)
    img_url = db.Column(db.String(120), nullable=False)
    feature_1 = db.Column(db.String(500), nullable=True)
    feature_2 = db.Column(db.String(500), nullable=True)
    feature_3 = db.Column(db.String(500), nullable=True)
    feature_4 = db.Column(db.String(500), nullable=True)
    feature_5 = db.Column(db.String(500), nullable=True)
    feature_6 = db.Column(db.String(500), nullable=True)
    feature_7 = db.Column(db.String(500), nullable=True)
    in_stock = db.Column(db.Boolean, nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "price": self.price,
            "name": self.name,
						"monthly":self.monthly,
            "desc": self.desc,
						"catagory": self.catagory,
						"sub_catagory": self.sub_catagory,
						"img_url": self.img_url,
            "feature_1": self.feature_1,
						"feature_2": self.feature_2,
						"feature_3": self.feature_3,
						"feature_4": self.feature_4,
						"feature_5": self.feature_5,
						"feature_6": self.feature_6,
						"feature_7": self.feature_7,
						"in_stock": self.in_stock
        }

class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    prod_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    is_completed = db.Column(db.Boolean, nullable=False)
    AMT = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    total_monthly = db.Column(db.Float, nullable=False)
    total_downpayment = db.Column(db.Float, nullable=False)
    monthly_due = db.Column(db.Boolean, nullable=False)
    downpayment_due = db.Column(db.Boolean, nullable=False)
    final_due = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    desc = db.Column(db.String(120), nullable=True)

    def toDict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "prod_id": self.prod_id,
						"is_completed": self.is_completed,
            "AMT": self.AMT,
						"total_cost": self.total_cost,
						"total_monthly": self.total_monthly,
						"total_downpayment": self.total_downpayment,
						"monthly_due": self.monthly_due,
						"downpayment_due": self.downpayment_due,
						"final_due": self.final_due,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S"),
						"desc": self.desc
        }

class wish_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    prod_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def toDict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "prod_id": self.prod_id
        }
