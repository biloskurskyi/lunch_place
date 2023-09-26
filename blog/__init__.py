"""Based on the Flask framework for managing a restaurant, menus, and orders, using an SQLite database."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'danger'


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
    app.config.from_pyfile('main/settings.py')
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from blog.main.routes import main

    app.register_blueprint(main)
    with app.app_context():
        db.create_all()

    return app


app_ctx = create_app()


def create_users():
    with app_ctx.app_context():
        from blog.models import User
        db.drop_all()
        db.create_all()

        users_data = [
            {'username': 'Mike', 'email': 'mike_admin@email.com', 'password': '1234'},
            {'username': 'John', 'email': 'john_user@email.com', 'password': '5678'},
            {'username': 'Alice', 'email': 'alice_user@email.com', 'password': 'abcd'},
            {'username': 'Tom', 'email': 'tom_user@email.com', 'password': '4444'},
            {'username': 'Io', 'email': 'io_user@email.com', 'password': 'ab12'},
        ]

        for user_info in users_data:
            hashed_password = bcrypt.generate_password_hash(user_info['password']).decode('utf-8')
            user = User(username=user_info['username'], email=user_info['email'], password=hashed_password)
            db.session.add(user)

        db.session.commit()


def create_restaurants():
    with app_ctx.app_context():
        from blog.models import Restaurant

        # Створення ресторанів
        restaurants_data = [
            {'name': 'Restaurant LA'},
            {'name': 'Restaurant Lviv'},
            {'name': 'Restaurant Old Style'},
        ]

        for restaurant_info in restaurants_data:
            restaurant = Restaurant(name=restaurant_info['name'])
            db.session.add(restaurant)

        db.session.commit()


def create_menu():
    with app_ctx.app_context():
        from blog.models import Menu

        today = datetime.date.today()

        day_of_week = today.strftime('%A')

        daily_menus = {
            'Monday': [
                {'name': 'Menu Item 1', 'price': 100, 'restaurant_id': 1},
                {'name': 'Menu Item 2', 'price': 150, 'restaurant_id': 1},
                {'name': 'Menu Item 3', 'price': 120, 'restaurant_id': 2},
                {'name': 'Menu Item 4', 'price': 80, 'restaurant_id': 2},
                {'name': 'Menu Item 5', 'price': 180, 'restaurant_id': 3},
                {'name': 'Menu Item 6', 'price': 140, 'restaurant_id': 3},
            ],
            'Tuesday': [
                {'name': 'Menu Item 7', 'price': 110, 'restaurant_id': 1},
                {'name': 'Menu Item 8', 'price': 160, 'restaurant_id': 1},
                {'name': 'Menu Item 9', 'price': 85, 'restaurant_id': 2},
                {'name': 'Menu Item 10', 'price': 190, 'restaurant_id': 3},
            ],
            'Wednesday': [
                {'name': 'Menu Item 12', 'price': 100, 'restaurant_id': 1},
                {'name': 'Menu Item 13', 'price': 120, 'restaurant_id': 2},
                {'name': 'Menu Item 14', 'price': 80, 'restaurant_id': 2},
                {'name': 'Menu Item 15', 'price': 80, 'restaurant_id': 2},
                {'name': 'Menu Item 16', 'price': 180, 'restaurant_id': 3},
                {'name': 'Menu Item 17', 'price': 140, 'restaurant_id': 3},
                {'name': 'Menu Item 18', 'price': 140, 'restaurant_id': 3},
            ],
            'Thursday': [
                {'name': 'Menu Item 19', 'price': 120, 'restaurant_id': 1},
                {'name': 'Menu Item 20', 'price': 125, 'restaurant_id': 2},
                {'name': 'Menu Item 21', 'price': 200, 'restaurant_id': 3},
            ],
            'Friday': [
                {'name': 'Menu Item 22', 'price': 120, 'restaurant_id': 1},
                {'name': 'Menu Item 23', 'price': 155, 'restaurant_id': 1},
                {'name': 'Menu Item 24', 'price': 125, 'restaurant_id': 2},
                {'name': 'Menu Item 25', 'price': 90, 'restaurant_id': 2},
                {'name': 'Menu Item 26', 'price': 200, 'restaurant_id': 3},
                {'name': 'Menu Item 27', 'price': 160, 'restaurant_id': 3},
            ],
            'Saturday': [
                {'name': 'Menu Item 28', 'price': 120, 'restaurant_id': 1},
                {'name': 'Menu Item 29', 'price': 125, 'restaurant_id': 2},
                {'name': 'Menu Item 30', 'price': 200, 'restaurant_id': 3},
            ],
            'Sunday': [
                {'name': 'Menu Item 31', 'price': 120, 'restaurant_id': 1},
                {'name': 'Menu Item 32', 'price': 125, 'restaurant_id': 2},
                {'name': 'Menu Item 33', 'price': 200, 'restaurant_id': 3},
            ]
        }

        todays_menu = daily_menus.get(day_of_week, [])

        Menu.query.delete()

        for menu_info in todays_menu:
            menu = Menu(name=menu_info['name'], price=menu_info['price'], restaurant_id=menu_info['restaurant_id'])
            db.session.add(menu)

        db.session.commit()
