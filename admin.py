import os
from flask import Blueprint, render_template, flash, send_from_directory, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import ShopItemsForm, OrderForm
from .models import Product, Order, Customer
from . import db

admin = Blueprint('admin', __name__)


# Helper: Check if current user is admin
def is_admin():
    return current_user.is_authenticated and current_user.id == 1


@admin.route('/media/<path:filename>')
def get_image(filename):
    media_folder = os.path.join(current_app.root_path, 'media')
    return send_from_directory(media_folder, filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if not is_admin():
        return render_template('404.html'), 403

    form = ShopItemsForm()
    if form.validate_on_submit():
        file = form.product_picture.data
        filename = secure_filename(file.filename)

        media_folder = os.path.join(current_app.root_path, 'media')
        os.makedirs(media_folder, exist_ok=True)
        file_path = os.path.join(media_folder, filename)
        file.save(file_path)

        new_item = Product(
            product_name=form.product_name.data,
            current_price=form.current_price.data,
            previous_price=form.previous_price.data,
            in_stock=form.in_stock.data,
            flash_sale=form.flash_sale.data,
            product_picture=f'/media/{filename}'
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            flash(f'{new_item.product_name} added successfully!', 'success')
            return redirect(url_for('admin.shop_items'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add product. Try again.', 'danger')
            print(f'Error adding product: {e}')

    return render_template('add_shop_items.html', form=form)


@admin.route('/shop-items')
#@login_required
def shop_items():
    if not is_admin():
        return render_template('404.html'), 403

    items = Product.query.order_by(Product.date_added.desc()).all()
    return render_template('shop_items.html', items=items)


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
#@login_required
def update_item(item_id):
    if not is_admin():
        return render_template('404.html'), 403

    item = Product.query.get_or_404(item_id)
    form = ShopItemsForm(obj=item)

    if form.validate_on_submit():
        if form.product_picture.data:
            file = form.product_picture.data
            filename = secure_filename(file.filename)
            media_folder = os.path.join(current_app.root_path, 'media')
            file_path = os.path.join(media_folder, filename)
            file.save(file_path)
            item.product_picture = f'/media/{filename}'

        item.product_name = form.product_name.data
        item.current_price = form.current_price.data
        item.previous_price = form.previous_price.data
        item.in_stock = form.in_stock.data
        item.flash_sale = form.flash_sale.data

        try:
            db.session.commit()
            flash(f'{item.product_name} updated successfully!', 'success')
            return redirect(url_for('admin.shop_items'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update product.', 'danger')
            print(f'Error updating product: {e}')

    return render_template('update_item.html', form=form, item=item)


@admin.route('/delete-item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    if not is_admin():
        return render_template('404.html'), 403

    item = Product.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Product deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete product.', 'danger')
        print(f'Error deleting product: {e}')

    return redirect(url_for('admin.shop_items'))


@admin.route('/view-orders')
@login_required
def order_view():
    if not is_admin():
        return render_template('404.html'), 403

    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template('view_orders.html', orders=orders)


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if not is_admin():
        return render_template('404.html'), 403

    form = OrderForm()
    order = Order.query.get_or_404(order_id)

    if form.validate_on_submit():
        order.status = form.order_status.data
        try:
            db.session.commit()
            flash(f'Order {order_id} updated successfully.', 'success')
            return redirect(url_for('admin.order_view'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update order.', 'danger')
            print(f'Error updating order: {e}')

    return render_template('order_update.html', form=form, order=order)


@admin.route('/customers')
@login_required
def display_customers():
    if not is_admin():
        return render_template('404.html'), 403

    customers = Customer.query.order_by(Customer.date_joined.desc()).all()
    return render_template('customers.html', customers=customers)


@admin.route('/admin-page')
@login_required
def admin_page():
    if not is_admin():
        return render_template('404.html'), 403

    return render_template('admin.html')










