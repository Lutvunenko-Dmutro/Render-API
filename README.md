# ⚡ Render REST API — Production Flask Microservice Template

> **Production-ready Flask REST API Boilerplate** для швидкого розгортання на **Render.com** з підтримкою **PostgreSQL**, **Swagger UI**, автоматичними юніт-тестами та **CI/CD пайплайном**.

[![CI Pipeline](https://github.com/Lutvunenko-Dmutro/Render-API/actions/workflows/ci.yml/badge.svg)](https://github.com/Lutvunenko-Dmutro/Render-API/actions)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-orange)](https://www.sqlalchemy.org/)
[![Render](https://img.shields.io/badge/Deploy-Render.com-46E3B7?logo=render)](https://render.com/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green?logo=openapi-initiative)](http://127.0.0.1:10000/docs)

---

## 🎯 Особливості проєкту

* **🚀 Cloud-Ready (Render / Railway):** Конфігурація `render.yaml` (Infrastructure as Code) з WSGI-сервером **Gunicorn**.
* **🗄️ Розумна робота з БД:** Підтримка **PostgreSQL** у хмарі та автоматичний fallback на **SQLite** для локальної розробки без додаткових налаштувань.
* **📖 Інтерактивна документація:** Вбудований **Swagger UI** (`/docs` або `/swagger`) та OpenAPI 3.0 специфікація (`/openapi.json`).
* **🩺 Healthcheck & Monitoring:** Ендпоінт `/health` з реальною перевіркою з'єднання з базою даних (`SELECT 1`) та часом безперервної роботи (uptime).
* **🧪 100% покриття тестами:** Автоматизований набір тестів (`unittest`) в ізольованій пам'яті (`sqlite:///:memory:`).
* **⚙️ CI/CD Пайплайн:** Автоматичний запуск тестів у **GitHub Actions** при кожному коміті.

---

## ⚡ Швидкий старт (Локально)

### 1. Клонування репозиторію
```bash
git clone https://github.com/Lutvunenko-Dmutro/Render-API.git
cd Render-API
```

### 2. Створення та активація віртуального оточення
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 4. Налаштування змінних оточення
Створіть файл `.env` на основі `.env.example`:
```bash
cp .env.example .env
```

Вміст `.env`:
```env
DATABASE_URL=sqlite:///data.db
PORT=10000
```

### 5. Запуск сервера
```bash
python app.py
```
👉 Сервер доступний за адресою: **`http://127.0.0.1:10000`**  
👉 Інтерактивна документація Swagger: **`http://127.0.0.1:10000/docs`**

---

## 🧪 Запуск автоматичних тестів

```bash
python -m unittest discover tests -v
```

---

## 🔌 Огляд API Ендпоінтів

| Метод | URL | Опис | Формат відповіді |
|---|---|---|---|
| `GET` | `/` | Головний привітальний ендпоінт | JSON |
| `GET` | `/health` | Перевірка стану сервера та підключення до БД | JSON |
| `GET` | `/docs` | Інтерактивна документація Swagger UI | HTML |
| `GET` | `/openapi.json` | OpenAPI 3.0 специфікація | JSON |
| `GET` | `/products` | Отримати список усіх продуктів | JSON Array |
| `POST` | `/products` | Створити новий продукт (`{"name": "..."}`) | JSON |
| `GET` | `/products/<id>` | Отримати продукт за ID | JSON |
| `DELETE`| `/products/<id>` | Видалити продукт за ID | JSON |
| `GET` | `/api/v1/productentitiestool-ui-admin/partner/getAll` | Інтеграційний ендпоінт партнерів | JSON Array |

---

## ☁️ Деплой на Render.com

Проєкт містить файл `render.yaml` для миттєвого розгортання (Blueprint):

1. Зареєструйтесь на [Render.com](https://render.com/).
2. Натисніть **New** ➔ **Blueprint**.
3. Підключіть репозиторій `Render-API`.
4. Render автоматично підхопить `render.yaml`, встановить залежності та запустить сервіс через `gunicorn app:app`.

---

## 📁 Структура проєкту

```
Render-API/
├── .github/workflows/
│   └── ci.yml               # GitHub Actions CI/CD пайплайн
├── tests/
│   ├── __init__.py
│   └── test_app.py          # Автоматизовані юніт-тести
├── app.py                   # Головний файл Flask додатка, Swagger UI та ендпоінти
├── config.py                # Конфігурація бази даних з авто-конвертацією URI
├── models.py                # SQLAlchemy модель Product
├── render.yaml              # Конфігурація для хмарного деплою на Render
├── requirements.txt         # Залежності Python (Gunicorn, psycopg2-binary, Flask)
├── .env.example             # Приклад конфігурації оточення
├── .gitignore               # Виключення тимчасових файлів та баз даних
└── README.md                # Документація проєкту
```

---

## 👨‍💻 Автор
* **Литвиненко Дмитро** — *Backend Developer*  
* GitHub: [@Lutvunenko-Dmutro](https://github.com/Lutvunenko-Dmutro)