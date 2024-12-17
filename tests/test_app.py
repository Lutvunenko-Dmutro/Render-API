import unittest
from app import app, db, Product

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Створення таблиць в тестовій базі даних
        with app.app_context():
            db.create_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.data.decode(), "Hello, Render API!")
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        # Тест для створення продукту в базі
        with app.app_context():
            new_product = Product(name="Test Product")
            db.session.add(new_product)
            db.session.commit()
            product = Product.query.filter_by(name="Test Product").first()
            self.assertIsNotNone(product)
            self.assertEqual(product.name, "Test Product")

if __name__ == '__main__':
    unittest.main()
