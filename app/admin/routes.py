from flask import render_template, jsonify, request, flash, redirect, url_for
from app.admin import admin
from flask_login import login_required, current_user
from app import db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def index():
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    total_products = Product.query.count()
    total_users = User.query.count()
    
    return render_template('admin/index.html',
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_products=total_products,
                         total_users=total_users)

@admin.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/order/<int:order_id>/update', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if 'status' in data:
        order.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'})
    
    return jsonify({'error': 'Invalid request'}), 400

@admin.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin.route('/product/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            category=request.form['category']
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html')

@admin.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category = request.form['category']
        
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', product=product)

@admin.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin.products')) 