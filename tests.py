import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_get_products(client):
    response = client.get('/api/products')
    assert response.status_code == 200


def test_get_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200