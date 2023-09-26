"""This file runs tests using unittest and PyTests"""
import unittest
from blog import create_app, db, create_users, create_restaurants, create_menu
from blog.models import User, Restaurant, Menu


class TestBlogApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_users(self):
        create_users()
        user = User.query.filter_by(username='Mike').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'Mike')

    def test_create_restaurants(self):
        create_restaurants()
        restaurant = Restaurant.query.filter_by(name='Restaurant LA').first()
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, 'Restaurant LA')

    def test_create_menu(self):
        create_restaurants()
        create_menu()
        menu_item = Menu.query.first()
        self.assertIsNotNone(menu_item)

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        create_users()
        create_restaurants()
        create_menu()
        self.client.post('/login', data={'email': 'mike_admin@email.com', 'password': '1234'})
        menu_item_id = 1
        response = self.client.post(f'/order_menu_item/{menu_item_id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/restaurant/Restaurant%20LA')

    def test_account_route_authenticated(self):
        create_users()
        self.client.post('/login', data={'email': 'mike_admin@email.com', 'password': '1234'})
        response = self.client.get('/account')
        self.assertEqual(response.status_code, 200)

    def test_account_route_unauthenticated(self):
        response = self.client.get('/account')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login?next=%2Faccount')


if __name__ == '__main__':
    unittest.main()
