from flask import Flask
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

@app.route('/')
def home():
    return "Hello, Render API!"

if __name__ == '__main__':
    # Створення таблиць у базі даних
    with app.app_context():
        db.create_all()

    port = os.getenv('PORT', 10000)  # порт для Render
    app.run(host='0.0.0.0', port=port, debug=False)  # відключення debug mode
