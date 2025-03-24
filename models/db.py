from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()


class Product(db.Model):
    """Product Table"""
    __tablename__ = 'products'

    product_id = db.Column(db.String(50), primary_key=True)  # Use product_id as PK
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'



class Category(db.Model):
    """Category Table"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
