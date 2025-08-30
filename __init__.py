import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
DB_NAME = 'database.sqlite3'

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'  # Replace with env var in production
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.root_path, DB_NAME)}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Import models to ensure they're registered
    from .models import Customer, Cart, Product, Order

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))

    # Register Blueprints
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Custom error pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Create the database if needed
    create_database(app)

    return app


def create_database(app):
    db_path = os.path.join(app.root_path, DB_NAME)
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('✔ Database created successfully at', db_path)


