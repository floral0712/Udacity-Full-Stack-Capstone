from sqlalchemy import Column, String, create_engine, Float, ForeignKey, Integer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json
import os
from flask_migrate import Migrate


# IN LOCAL

# database_url="postgres://yaoxiao@localhost:5432/capstone"


database_url = "postgres://gtstnxqadsjulf:57a230c0fb9987a10f2e7976c57587db7d878227b5b075bd9421f3025c8d7df9@ec2-52-202-198-60.compute-1.amazonaws.com:5432/d735kbcocvrh39"

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


order_dessert = db.Table(
    'order_dessert',
    Column('order_id', Integer, ForeignKey('Order.id'), primary_key=True),
    Column('dessert_id', Integer, ForeignKey('Dessert.id'), primary_key=True))


class Dessert(db.Model):
    __tablename__ = 'Dessert'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    def _init__(self, name, price):
        self.name = name
        self.price = price

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "dessert": self.name,
            "price": str(self.price)
        }


class Order(db.Model):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    customer = Column(String)
    items = relationship('Dessert', secondary=order_dessert,
                         backref=db.backref('order', lazy=True))

    def __init__(self, customer):
        self.customer = customer

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "customer": self.customer,
            "dessert": [dessert.name for dessert in self.items]
        }
