from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.cart import CartItem
from app.models.product import Product

cart = Blueprint('cart', __name__)

@cart.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get_or_404(product_id)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Item added to cart'})

@cart.route('/cart/view')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'items': [item.to_dict() for item in cart_items],
        'total': sum(item.product.price * item.quantity for item in cart_items)
    })

@cart.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    return jsonify({'message': 'Cart updated'})

@cart.route('/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}) 