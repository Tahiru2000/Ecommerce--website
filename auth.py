from flask import Blueprint, render_template, flash, redirect, url_for, request
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password1.data

        existing_user = Customer.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered. Please use a different one.', 'danger')
            return render_template('signup.html', form=form)

        new_customer = Customer(email=email, username=username)
        new_customer.password = password  # uses property setter in model

        try:
            db.session.add(new_customer)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account.', 'danger')
            print("Signup error:", e)

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()
        if customer and customer.verify_password(password):
            login_user(customer)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('views.home'))  # Adjust this to your actual home route
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('views.home'))  # Adjust as needed


@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    if current_user.id != customer_id:
        flash("You are not authorized to view this profile.", "warning")
        return redirect(url_for('views.home'))

    customer = Customer.query.get_or_404(customer_id)
    return render_template('profile.html', customer=customer)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    if current_user.id != customer_id:
        flash("You are not authorized to change this password.", "warning")
        return redirect(url_for('views.home'))

    form = PasswordChangeForm()
    customer = Customer.query.get_or_404(customer_id)

    if form.validate_on_submit():
        if customer.verify_password(form.current_password.data):
            customer.password = form.new_password.data  # uses password setter
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('auth.profile', customer_id=customer.id))
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('change_password.html', form=form)








