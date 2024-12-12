import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Product, CartItem, Order, OrderItem

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True) 