# This file aggregates all Flask blueprints and provides a centralized function
# to register them in the Flask application instance.

from app.blueprints.auth import auth_bp
from app.blueprints.admin import admin_bp
from app.blueprints.student import student_bp
from app.blueprints.teacher import teacher_bp

def register_blueprints(app):
    """
    Registers all blueprints to the Flask app instance.

    Args:
        app (Flask): The Flask application object
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
