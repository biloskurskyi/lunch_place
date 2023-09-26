"""This code allows users to authenticate, view the restaurant's menu, and place orders using links."""
from flask import render_template, request, redirect, flash, url_for, Blueprint, jsonify
from blog import db
from blog.main.forms import LoginForm
from blog.models import User, Restaurant, Menu, Order
from blog.models import check_password_hash
from flask_login import login_user, current_user, login_required, logout_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', title='Main')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            flash('Login failed, please check your email or password', 'danger')
    return render_template('login.html', title='Authorization', legend='Enter', form=form)


@main.route('/account')
@login_required
def account():
    restaurants = Restaurant.query.all()
    return render_template('account.html', title='Account', current_user=current_user, restaurants=restaurants)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/account/restaurant/<restaurant_name>')
@login_required
def restaurant(restaurant_name):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    if restaurant:
        menu_items = Menu.query.filter_by(restaurant_id=restaurant.id).all()
        return render_template('restaurant.html', title=restaurant.name, restaurant=restaurant, menu_items=menu_items)
    else:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('main.account'))


orders_file = "orders.txt"


@main.route('/order_menu_item/<int:menu_item_id>', methods=['POST', 'DELETE'])
@login_required
def order_menu_item(menu_item_id):
    if request.method == 'POST':
        menu_item = Menu.query.get_or_404(menu_item_id)
        if not menu_item:
            flash('Menu not found', 'danger')
        elif menu_item.ordered_by_user(current_user):
            order = Order.query.filter_by(menu_id=menu_item.id, user_id=current_user.id).first()
            db.session.delete(order)
            db.session.commit()
            flash('Your order has been canceled', 'info')
            with open(orders_file, 'r') as file:
                lines = file.readlines()
            with open(orders_file, 'w') as file:
                for line in lines:
                    if f"User: {current_user.username}, Menu Item: {menu_item.name}" not in line:
                        file.write(line)
        else:
            order = Order(user_id=current_user.id, menu_id=menu_item.id)
            db.session.add(order)
            db.session.commit()
            flash('The menu is ordered', 'success')
            with open(orders_file, 'a') as file:
                file.write(f"User: {current_user.username}, Menu Item: {menu_item.name}\n")

    return redirect(url_for('main.restaurant', restaurant_name=menu_item.restaurant.name))
