import os
import sys
import pytest

# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.product import Product

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        # Create test admin user
        admin = User(
            username='testadmin',
            email='testadmin@example.com',
            is_admin=True
        )
        admin.set_password('testpass123')
        db.session.add(admin)
        
        # Create test product
        product = Product(
            name='Test Product',
            description='Test Description',
            price=99.99,
            stock=10,
            category='Test Category'
        )
        db.session.add(product)
        db.session.commit()
        
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Our Store' in response.data

def test_products_page(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert b'Test Product' in response.data

def test_admin_login(client):
    # Test login with correct credentials
    response = client.post('/auth/login', data={
        'email': 'testadmin@example.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_add_to_cart(client):
    # First login
    client.post('/auth/login', data={
        'email': 'testadmin@example.com',
        'password': 'testpass123'
    })
    
    # Then add item to cart
    response = client.post('/cart/add', json={
        'product_id': 1,
        'quantity': 1
    })
    assert response.status_code == 200
    assert b'Item added to cart' in response.data

def test_view_cart(client):
    # First login
    client.post('/auth/login', data={
        'email': 'testadmin@example.com',
        'password': 'testpass123'
    })
    
    # View cart
    response = client.get('/cart/view')
    assert response.status_code == 200 