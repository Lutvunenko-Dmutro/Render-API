from flask import Flask, jsonify, request, render_template_string
from models import db, Product
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Ініціалізація бази даних
db.init_app(app)

start_time = time.time()

# OpenAPI 3.0 Специфікація
OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Render Flask REST API",
        "description": "Production-ready Flask Microservice Template with PostgreSQL & automated tests.",
        "version": "1.0.0"
    },
    "servers": [
        {"url": "/", "description": "Current Server"}
    ],
    "paths": {
        "/": {
            "get": {
                "summary": "Root Welcome Endpoint",
                "responses": {
                    "200": {"description": "Welcome message"}
                }
            }
        },
        "/health": {
            "get": {
                "summary": "Health Check & Database Connectivity",
                "responses": {
                    "200": {"description": "Service is healthy and DB is connected"}
                }
            }
        },
        "/products": {
            "get": {
                "summary": "Get all products",
                "responses": {
                    "200": {"description": "List of products"}
                }
            },
            "post": {
                "summary": "Create a new product",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "example": "MacBook Pro M3"}
                                },
                                "required": ["name"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Product created successfully"},
                    "400": {"description": "Validation error"}
                }
            }
        },
        "/products/{id}": {
            "get": {
                "summary": "Get product by ID",
                "parameters": [
                    {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {"description": "Product found"},
                    "404": {"description": "Product not found"}
                }
            },
            "delete": {
                "summary": "Delete product by ID",
                "parameters": [
                    {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {"description": "Product deleted"},
                    "404": {"description": "Product not found"}
                }
            }
        },
        "/api/v1/productentitiestool-ui-admin/partner/getAll": {
            "get": {
                "summary": "Get all partners integration",
                "responses": {
                    "200": {"description": "List of partners"}
                }
            }
        }
    }
}

SWAGGER_UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Swagger UI - Render API</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
    <style>
        body { margin: 0; padding: 0; background: #fafafa; font-family: sans-serif; }
        .top-banner { background: #0f172a; color: white; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; }
        .top-banner h1 { margin: 0; font-size: 18px; font-weight: 600; }
        .top-banner a { color: #38bdf8; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div class="top-banner">
        <h1>⚡ Render REST API — Interactive Documentation</h1>
        <a href="https://github.com/Lutvunenko-Dmutro/Render-API" target="_blank">GitHub Repository ↗</a>
    </div>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.onload = () => {
            window.ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            });
        };
    </script>
</body>
</html>
"""

# Маршрути документації
@app.route('/openapi.json')
def openapi_json():
    return jsonify(OPENAPI_SPEC)

@app.route('/docs')
@app.route('/swagger')
def swagger_ui():
    return render_template_string(SWAGGER_UI_TEMPLATE)

# Головний маршрут
@app.route('/')
def home():
    return jsonify({
        "message": "Hello, Render API!",
        "status": "online",
        "documentation": "/docs",
        "healthcheck": "/health"
    })

# Healthcheck & Metrics
@app.route('/health')
def health():
    db_status = "connected"
    try:
        db.session.execute(db.text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "uptime_seconds": int(time.time() - start_time),
        "environment": "production" if os.getenv('RENDER') else "development"
    }), 200 if db_status == "connected" else 503

# Продукти CRUD
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"error": "Поле 'name' є обов'язковим"}), 400
    
    product = Product(name=data['name'].strip())
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Продукт #{product_id} успішно видалено"}), 200

# Партнери
@app.route('/api/v1/productentitiestool-ui-admin/partner/getAll', methods=['GET'])
def get_all_partners():
    partners = [{"id": 1, "name": "Partner 1"}, {"id": 2, "name": "Partner 2"}]
    return jsonify(partners)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
