from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Import blueprints
        from app.routes import main
        from app.auth import auth
        from app.admin import admin
        from app.cart import cart
        from app.checkout import checkout

        # Register blueprints
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(admin)
        app.register_blueprint(cart)
        app.register_blueprint(checkout)

        # Create database tables
        db.create_all()

        # Create admin user if it doesn't exist
        from app.models.user import User
        admin_user = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email=app.config['ADMIN_EMAIL'],
                is_admin=True
            )
            admin_user.set_password('admin123')  # Default password, should be changed
            db.session.add(admin_user)
            db.session.commit()

        # Add sample products if none exist
        from app.models.product import Product
        if Product.query.count() == 0:
            sample_products = [
                {
                    'name': 'Laptop Pro',
                    'description': 'High-performance laptop for professionals',
                    'price': 1299.99,
                    'stock': 10,
                    'category': 'Electronics'
                },
                {
                    'name': 'Wireless Headphones',
                    'description': 'Premium wireless headphones with noise cancellation',
                    'price': 199.99,
                    'stock': 20,
                    'category': 'Electronics'
                },
                {
                    'name': 'Smart Watch',
                    'description': 'Feature-rich smartwatch with health tracking',
                    'price': 299.99,
                    'stock': 15,
                    'category': 'Electronics'
                }
            ]
            
            for product_data in sample_products:
                product = Product(**product_data)
                db.session.add(product)
            
            db.session.commit()

        return app 