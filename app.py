from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Завантаження змінних оточення з .env
load_dotenv()

app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

@app.route('/')
def home():
    return "Hello, Render API!"

if __name__ == '__main__':
    port = os.getenv('PORT', 10000)  # порт для Render
    app.run(host='0.0.0.0', port=port, debug=False)  # відключення debug mode
