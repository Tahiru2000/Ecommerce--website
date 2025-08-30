from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, FloatField, PasswordField, EmailField,
    BooleanField, SubmitField, SelectField
)
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[
        DataRequired(),
        EqualTo('password1', message='Passwords must match.')
    ])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    change_password = SubmitField('Change Password')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired(), NumberRange(min=0)])
    previous_price = FloatField('Previous Price', validators=[DataRequired(), NumberRange(min=0)])
    in_stock = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    flash_sale = BooleanField('Flash Sale')
    
    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update Product')


class OrderForm(FlaskForm):
    order_status = SelectField(
        'Order Status',
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Out for delivery', 'Out for delivery'),
            ('Delivered', 'Delivered'),
            ('Canceled', 'Canceled')
        ],
        validators=[DataRequired()]
    )
    update = SubmitField('Update Status')






