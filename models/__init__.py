from .db import db


def init_db(app):
    """Initialize the database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
