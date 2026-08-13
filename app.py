from flask import Flask, jsonify, request
from models import db, Product
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Ініціалізація бази даних
db.init_app(app)

# Головний маршрут
@app.route('/')
def home():
    return "Hello, Render API!"

# Маршрут для отримання всіх партнерів (тестовий)
@app.route('/api/v1/productentitiestool-ui-admin/partner/getAll', methods=['GET'])
def get_all_partners():
    partners = [{"id": 1, "name": "Partner 1"}, {"id": 2, "name": "Partner 2"}]
    return jsonify(partners)

# Маршрути для продуктів
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    
    product = Product(name=data['name'])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
