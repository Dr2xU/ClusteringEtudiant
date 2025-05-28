import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, render_template, redirect, url_for
from app.config import Config
from app.extensions import db
from app.blueprints import auth_bp,admin_bp, teacher_bp, student_bp


def create_app(config_class=Config):
    """
    Flask application factory.
    Creates and configures the app instance.

    Args:
        config_class (Config): Configuration class to use

    Returns:
        Flask: Configured Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)

    # Register blueprints directly
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)

    # Optional: Redirect root to login page
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    # Create database tables at startup
    with app.app_context():
        db.create_all()

    return app
