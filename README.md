# 🖥️ Fashion E-Commerce Backend

This is the backend for the Fashion E-Commerce Website. Built with Flask and SQLAlchemy, it provides secure REST APIs for user management, products, categories, orders, invoices, and role-based authentication using JWT.

---

## 🚀 Features

- JWT-based Authentication and Authorization
- Role-based Access Control (User & Admin)
- Product and Category Management
- Shopping Cart and Orders
- Invoicing System
- SQLite (dev) / PostgreSQL (prod)
- CORS enabled for frontend connection

---

## 🧰 Tech Stack

- Python 3.11
- Flask
- Flask-JWT-Extended
- SQLAlchemy & Flask-Migrate
- SQLite / PostgreSQL
- Marshmallow (optional for serialization)

---

## 📦 Setup Instructions

### 1. Clone the repo

``
git clone [https://github.com/irarubrian/fashion-design-backend/tree/Development]
cd fashion-ecommerce/backend

### 2.Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

##4. Configure Environment Variables
Create a .env file (or set variables directly):

FLASK_APP=app.py
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db

### 5. Set up the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

### 6. Run the server
flask run
