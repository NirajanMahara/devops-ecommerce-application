from flask import Blueprint, render_template
from app.models.product import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.limit(6).all()
    return render_template('index.html', products=products)

@main.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products) 