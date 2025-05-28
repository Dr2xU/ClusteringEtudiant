import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration class loaded by Flask.
    Reads values from environment variables with sensible defaults.
    """
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-default-key')  # Used for session security

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///clustering.db')  # DB path
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event notifications (improves performance)

    # Flask environment
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')  # development or production
