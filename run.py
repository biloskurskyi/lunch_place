"""The file is a Python script that creates a Flask web application for a blog,
initializes initial data, schedules a daily task to clear an 'orders.txt' file,
and runs the web application in debug mode on port 9999."""
from blog import create_app, create_users, create_restaurants, create_menu
import schedule
import time
import threading


def clear_orders_file():
    with open('orders.txt', 'w') as file:
        pass


def schedule_clear_orders():
    schedule.every().day.at('23:00').do(clear_orders_file)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    create_users()
    create_restaurants()
    create_menu()
    schedule_thread = threading.Thread(target=schedule_clear_orders)
    schedule_thread.start()
    app = create_app()
    app.run(debug=True, port='9998')
