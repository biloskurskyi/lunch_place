"""This code creates the fundamental structure of the database for managing restaurants, menus, and orders.
It also includes methods for working with user passwords and checking the status of menu orders."""
from flask_bcrypt import check_password_hash
from flask_login import UserMixin
from blog import db, bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password, hashed_password):
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'User({self.username},{self.email},{self.password})'


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Restaurant({self.name})'


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __init__(self, name, price, restaurant_id):
        self.name = name
        self.price = price
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return f'Menu({self.name}, {self.price})'

    def ordered_by_user(self, user):
        return Order.query.filter_by(menu_id=self.id, user_id=user.id).first() is not None


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    ordered = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, menu_id):
        self.user_id = user_id
        self.menu_id = menu_id
