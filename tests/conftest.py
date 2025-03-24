import pytest
from main import app, db
from models.db import Category, Product

@pytest.fixture
def client():
    """Create a test client and database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # to create the tables
        yield client

        # Cleanup
        with app.app_context():
            db.drop_all()
