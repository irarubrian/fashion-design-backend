# 🛍️ Fashion E-Commerce Backend

This is the backend API for a stylish fashion e-commerce web application, built using **Flask** and **SQLAlchemy**. It provides user registration/login, product management, shopping cart, checkout, and admin functionality.

---

## 🚀 Features

- 👤 User Registration & Login
- 🛒 Shopping Cart Management
- 📦 Product & Category Listings
- ✅ Checkout & Order Creation
- 📄 Invoice Generation
- 🔐 Admin CRUD for Products

---

## 📁 Project Structure

fashion-backend/ │ ├── app.py # App entry point ├── models/ # SQLAlchemy models │ └── models.py ├── routes/ # Flask API routes │ └── routes.py ├── seed/ # Seed script for DB │ └── seed_data.py ├── migrations/ # Flask-Migrate files ├── requirements.txt # Python dependencies └── README.md # You're here!

## 🛠️ Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <https://github.com/irarubrian/fashion-design-backend>
cd fashion-backend
2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
# OR
venv\Scripts\activate      # Windows
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Set Environment Variables


Create a .env file or set these manually:

FLASK_APP=app.py
FLASK_ENV=development

5️⃣ Run Migrations
flask db init            # Only once
flask db migrate -m "Initial migration"
flask db upgrade
6️⃣ Seed the Database
python seed/seed_data.py
This adds:

Sample users (admin & customer)

Categories & products

Address, cart item, order, and invoice

7️⃣ Run the Server
flask run
Server will run on:
📍 http://127.0.0.1:5000/

📬 API Endpoints
🔐 Auth

Method	Endpoint	Description
POST	/register	Register new user
POST	/login	Login user
📦 Products & Categories

Method	Endpoint	Description
GET	/products	List all products
GET	/categories	List all categories
🛒 Cart

Method	Endpoint	Description
GET	/cart/<user_id>	View cart items
POST	/cart/add	Add item to cart
✅ Checkout & Orders

Method	Endpoint	Description
POST	/checkout	Place an order
GET	/orders/<user_id>	View past orders
🛠️ Admin

Method	Endpoint	Description
POST	/admin/products	Add new product
PUT	/admin/products/<id>	Update a product
DELETE	/admin/products/<id>	Delete a product
🧪 Testing with Postman
You can test all endpoints using Postman by sending HTTP requests to:

http://127.0.0.1:5000/

👥 Authors
👨‍💻 Diyuu – Project Lead & Backend Developer
👨‍💻 Brian iraru- scrum master &  backend developer 

📜 License
This project is licensed under the MIT License.

Copyright <2025> <Hamdi Aden>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.








