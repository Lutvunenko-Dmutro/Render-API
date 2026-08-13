import unittest
from app import app, db, Product

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.data.decode(), "Hello, Render API!")
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        with app.app_context():
            new_product = Product(name="Test Product")
            db.session.add(new_product)
            db.session.commit()
            product = Product.query.filter_by(name="Test Product").first()
            self.assertIsNotNone(product)
            self.assertEqual(product.name, "Test Product")

    def test_get_partners(self):
        response = self.app.get('/api/v1/productentitiestool-ui-admin/partner/getAll')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_products_api(self):
        res = self.app.post('/products', json={"name": "Laptop"})
        self.assertEqual(res.status_code, 201)
        
        get_res = self.app.get('/products')
        self.assertEqual(get_res.status_code, 200)
        items = get_res.get_json()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], "Laptop")

if __name__ == '__main__':
    unittest.main()
