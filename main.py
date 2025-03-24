from flask import Flask, render_template, request, redirect, url_for, flash
from config import config
from models import init_db, db
from models.db import Product, Category
from models.factory import ProductFactory, CategoryFactory
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize the database
init_db(app)


@app.route('/')
def index():
    """Display all products"""
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Add new product"""
    
    if request.method == 'POST':
        try:
            # Retrieve form data
            product_id = request.form.get('product_id', '').strip()
            name = request.form.get('name', '').strip()
            price = request.form.get('price', '').strip()
            quantity = request.form.get('quantity', '').strip()
            category_id = request.form.get('category', '').strip()

            #   all fields are filled
            if not all([product_id, name, price, quantity, category_id]):
                flash("All fields are required.", "warning")
                return redirect(url_for('add_product'))

            #  Validate data and types
            try:
                price = float(price)
                quantity = int(quantity)
                category_id = int(category_id)
            except ValueError:
                flash("Invalid data format. Check your inputs.", "danger")
                return redirect(url_for('add_product'))

            #  Check for duplicate ids
            existing_product = Product.query.get(product_id)
            if existing_product:
                flash("Product ID already exists.", "warning")
                return redirect(url_for('add_product'))

            # Use factory pattern to create product
            product = ProductFactory.create_product(
                product_id, name, price, quantity, category_id
            )

            # Save to database
            new_product = Product(
                product_id=product.get_product_id(),
                name=product.get_name(),
                price=product.get_price(),
                quantity=product.get_quantity(),
                category_id=product.get_category_id()
            )

            db.session.add(new_product)
            db.session.commit()
            
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))

        except IntegrityError:
            db.session.rollback()
            flash("Product ID already exists.", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)


#  Update Product Route
@app.route('/update_product/<string:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    """Update an existing product"""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        try:
            product.name = request.form['name'].strip()
            product.price = float(request.form['price'].strip())
            product.quantity = int(request.form['quantity'].strip())
            product.category_id = int(request.form['category'].strip())

            db.session.commit()
            flash('Product updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('index'))

    categories = Category.query.all()
    return render_template('update_product.html', product=product, categories=categories)


#  Delete Product Route
@app.route('/delete_product/<string:product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product"""
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('index'))


#  Add Category Route
@app.route('/categories', methods=['GET'])
def list_categories():
    """Display all categories"""
    categories = Category.query.all()  # Fetch all categories
    return render_template('category.html', categories=categories)

# Route: Add Category with Duplicate Check
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    """Add new category"""
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            description = request.form['description'].strip()

            # Check for duplicate name
            existing_category = Category.query.filter_by(name=name).first()
            
            if existing_category:
                flash('Category name already exists!', 'warning')
                return redirect(url_for('list_categories'))

            # Add new category
            new_category = Category(name=name, description=description)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('list_categories'))

    categories = Category.query.all()
    return render_template('category.html', categories=categories)

# Route: Update Category with Duplicate Check
@app.route('/update_category/<int:category_id>', methods=['GET', 'POST'])
def update_category(category_id):
    """Update an existing category"""
    category = Category.query.get_or_404(category_id)

    if request.method == 'POST':
        new_name = request.form['name'].strip()
        new_description = request.form['description'].strip()

        # Check for duplicate name (excluding the current category)
        existing_category = Category.query.filter(
            Category.name == new_name, 
            Category.id != category_id
        ).first()

        if existing_category:
            flash('Category name already exists!', 'warning')
            return redirect(url_for('update_category', category_id=category_id))

        try:
            category.name = new_name
            category.description = new_description

            db.session.commit()
            flash('Category updated successfully!', 'success')
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('list_categories'))

    return render_template('update_category.html', category=category)

# Route: Delete Category
@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """Delete a category"""
    category = Category.query.get_or_404(category_id)

    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('list_categories'))

# Create Database Tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
