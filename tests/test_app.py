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
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "online")

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")

    def test_swagger_and_openapi(self):
        res_docs = self.app.get('/docs')
        self.assertEqual(res_docs.status_code, 200)
        self.assertIn(b"Swagger UI", res_docs.data)

        res_spec = self.app.get('/openapi.json')
        self.assertEqual(res_spec.status_code, 200)
        spec = res_spec.get_json()
        self.assertEqual(spec["openapi"], "3.0.3")

    def test_create_and_delete_product(self):
        # Create product
        res = self.app.post('/products', json={"name": "MacBook Pro M3"})
        self.assertEqual(res.status_code, 201)
        prod_id = res.get_json()["id"]

        # Get all products
        res_list = self.app.get('/products')
        self.assertEqual(res_list.status_code, 200)
        self.assertEqual(len(res_list.get_json()), 1)

        # Get product by ID
        res_item = self.app.get(f'/products/{prod_id}')
        self.assertEqual(res_item.status_code, 200)
        self.assertEqual(res_item.get_json()["name"], "MacBook Pro M3")

        # Delete product
        res_del = self.app.delete(f'/products/{prod_id}')
        self.assertEqual(res_del.status_code, 200)

        # Confirm deleted
        res_after = self.app.get(f'/products/{prod_id}')
        self.assertEqual(res_after.status_code, 404)

    def test_get_partners(self):
        response = self.app.get('/api/v1/productentitiestool-ui-admin/partner/getAll')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

if __name__ == '__main__':
    unittest.main()
