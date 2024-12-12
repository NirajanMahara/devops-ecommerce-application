from flask import render_template
from app.routes import main
from app.models.product import Product

@main.route('/')
def index():
    products = Product.query.limit(6).all()
    return render_template('index.html', products=products)

@main.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products) 