from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product

checkout = Blueprint('checkout', __name__)

@checkout.route('/checkout', methods=['GET'])
@login_required
def checkout_page():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('main.products'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@checkout.route('/checkout/process', methods=['POST'])
@login_required
def process_checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    # Validate stock availability
    for item in cart_items:
        if item.quantity > item.product.stock:
            return jsonify({
                'error': f'Not enough stock for {item.product.name}. Available: {item.product.stock}'
            }), 400

    # Get shipping address from form
    shipping_address = request.form.get('shipping_address')
    if not shipping_address:
        return jsonify({'error': 'Shipping address is required'}), 400

    try:
        # Calculate total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_address=shipping_address
        )
        db.session.add(order)

        # Create order items and update stock
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)

            # Update product stock
            cart_item.product.stock -= cart_item.quantity

        # Clear cart
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': order.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@checkout.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@checkout.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('order_detail.html', order=order) 