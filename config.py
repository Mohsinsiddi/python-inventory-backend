import os

# Flask Configuration
class Config:
    """Base configuration for Flask"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

# Environment dictionary for easy switching
config = {
    'development': Config
}
