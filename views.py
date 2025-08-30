from flask import Blueprint, app, render_template, flash, redirect, request, jsonify, url_for
from .models import Product, Cart, Order
from flask_login import login_required, current_user
from . import db
from intasend import APIService
from flask import render_template, session



views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'YOUR_PUBLISHABLE_KEY'
API_TOKEN = 'YOUR_API_TOKEN'
DELIVERY_FEE = 200  # better to use a constant


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True).all()
    cart = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else []
    return render_template('home.html', items=items, cart=cart)

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get_or_404(item_id)
    cart_item = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()

    try:
        if cart_item:
            cart_item.quantity += 1
            flash(f'Quantity of {cart_item.product.product_name} has been updated.')
        else:
            cart_item = Cart(quantity=1, product_link=item_to_add.id, customer_link=current_user.id)
            db.session.add(cart_item)
            flash(f'{item_to_add.product_name} added to cart.')

        db.session.commit()
    except Exception as e:
        print('Error updating cart:', e)
        flash('An error occurred while updating the cart.')

    return redirect(request.referrer or url_for('views.home'))


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    return render_template('cart.html', cart=cart, amount=amount, total=amount + DELIVERY_FEE)


@views.route('/plus-cart')
@login_required
def plus_cart():
    cart_id = request.args.get('cart_id')
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.customer_link != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    cart_item.quantity += 1
    db.session.commit()
    return calculate_cart_totals(cart_item)


@views.route('/minus-cart')
@login_required
def minus_cart():
    cart_id = request.args.get('cart_id')
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.customer_link != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)

    db.session.commit()
    return calculate_cart_totals(cart_item)


@views.route('/remove-cart')
@login_required
def remove_cart():
    cart_id = request.args.get('cart_id')
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.customer_link != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(cart_item)
    db.session.commit()
    return calculate_cart_totals(cart_item)


def calculate_cart_totals(reference_item):
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    return jsonify({
        'quantity': sum(item.quantity for item in cart),
        'amount': amount,
        'total': amount + DELIVERY_FEE
    })


@views.route('/place-order')
@login_required
def place_order():
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.')
        return redirect(url_for('views.home'))

    try:
        total = sum(item.product.current_price * item.quantity for item in cart_items)

        service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
        payment = service.collect.mpesa_stk_push(
            phone_number='YOUR_NUMBER',
            email=current_user.email,
            amount=total + DELIVERY_FEE,
            narrative='Purchase of goods'
        )

        for item in cart_items:
            order = Order(
                quantity=item.quantity,
                price=item.product.current_price,
                status=payment['invoice']['state'].capitalize(),
                payment_id=payment['id'],
                product_link=item.product_link,
                customer_link=item.customer_link
            )

            product_obj = Product.query.get(item.product_link)
            if product_obj:
                product_obj.in_stock = max(0, product_obj.in_stock - item.quantity)

            db.session.add(order)
            db.session.delete(item)

        db.session.commit()
        flash('Order placed successfully!')
        return redirect(url_for('views.order'))

    except Exception as e:
        print('Order error:', e)
        flash('An error occurred while placing the order.')
        return redirect(url_for('views.home'))


@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)


@views.route('/search', methods=['GET', 'POST'])
def search():
    items = []
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()

    cart = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else []
    return render_template('search.html', items=items, cart=cart)















