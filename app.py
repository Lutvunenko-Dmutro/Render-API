from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Завантаження змінних оточення з .env
load_dotenv()

app = Flask(__name__)

# Налаштування бази даних
app.config.from_object('config.Config')  # Завантаження конфігурацій з config.py

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# Головний маршрут
@app.route('/')
def home():
    return "Hello, Render API!"

# Маршрут для отримання всіх партнерів (наприклад, для тесту)
@app.route('/api/v1/productentitiestool-ui-admin/partner/getAll', methods=['GET'])
def get_all_partners():
    # Логіка для отримання всіх партнерів
    # Тут може бути реальна логіка доступу до бази даних для отримання партнерів
    partners = [{"id": 1, "name": "Partner 1"}, {"id": 2, "name": "Partner 2"}]
    return jsonify(partners)

if __name__ == '__main__':
    # Створення таблиць у базі даних
    with app.app_context():
        db.create_all()

    port = os.getenv('PORT', 10000)  # порт для Render
    app.run(host='0.0.0.0', port=port, debug=False)  # відключення debug mode
