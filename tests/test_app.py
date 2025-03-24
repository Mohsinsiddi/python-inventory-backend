import pytest
from models.db import Category, Product, db

# Use home route page
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Products' in response.data
    assert b'Categories' in response.data

# testing adding category
def test_add_category(client):
    """Test adding a new category"""
    response = client.post('/add_category', data={
        'name': 'Test Category',
        'description': 'Test Description'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Category added successfully!' in response.data

    #Check if category was added to the database
    with client.application.app_context():
        category = Category.query.filter_by(name='Test Category').first()
        assert category is not None
        assert category.description == 'Test Description'

#test adding duplicate category
def test_duplicate_category(client):
    """Test duplicate category handling"""
    client.post('/add_category', data={
        'name': 'Duplicate Category',
        'description': 'Description 1'
    }, follow_redirects=True)

    response = client.post('/add_category', data={
        'name': 'Duplicate Category',
        'description': 'Description 2'
    }, follow_redirects=True)

    assert b'Category name already exists!' in response.data

#adding product
def test_add_product(client):
    """Test adding a new product"""
    
    # Create a category first to execuoi the producr
    client.post('/add_category', data={
        'name': 'Electronics',
        'description': 'Gadgets and Devices'
    }, follow_redirects=True)

    # Get the category ID
    with client.application.app_context():
        category = Category.query.filter_by(name='Electronics').first()

    response = client.post('/add_product', data={
        'product_id': 'P1001',
        'name': 'Laptop',
        'price': '1200.50',
        'quantity': '10',
        'category': str(category.id)
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Product added successfully!' in response.data

    # Check if product was added to the database
    with client.application.app_context():
        product = Product.query.filter_by(product_id='P1001').first()
        assert product is not None
        assert product.name == 'Laptop'

#  Test Duplicate Product ID
def test_duplicate_product_id(client):
    """Test adding a product with duplicate ID"""
    
    # Add a category
    client.post('/add_category', data={
        'name': 'Furniture',
        'description': 'Home Furniture'
    }, follow_redirects=True)

    # Get the category ID
    with client.application.app_context():
        category = Category.query.filter_by(name='Furniture').first()

    # Add first product
    client.post('/add_product', data={
        'product_id': 'P2001',
        'name': 'Chair',
        'price': '50.00',
        'quantity': '30',
        'category': str(category.id)
    }, follow_redirects=True)

    # Add product with same ID
    response = client.post('/add_product', data={
        'product_id': 'P2001',
        'name': 'Table',
        'price': '120.00',
        'quantity': '20',
        'category': str(category.id)
    }, follow_redirects=True)

    assert b'Product ID already exists' in response.data

#  Test Updating a Category
def test_update_category(client):
    """Test updating an existing category"""
    
    # Add a category
    client.post('/add_category', data={
        'name': 'Clothing',
        'description': 'Apparel and fashion'
    }, follow_redirects=True)

    # Get the category ID
    with client.application.app_context():
        category = Category.query.filter_by(name='Clothing').first()

    # Update the category
    response = client.post(f'/update_category/{category.id}', data={
        'name': 'Clothing Updated',
        'description': 'Updated description'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Category updated successfully!' in response.data

    # Verify the update
    with client.application.app_context():
        updated_category = Category.query.get(category.id)
        assert updated_category.name == 'Clothing Updated'

#  Test Deleting a Category
def test_delete_category(client):
    """Test deleting a category"""

    # Add a category
    client.post('/add_category', data={
        'name': 'Books',
        'description': 'Fiction and non-fiction'
    }, follow_redirects=True)

    # Get the category ID
    with client.application.app_context():
        category = Category.query.filter_by(name='Books').first()

    # Delete the category
    response = client.post(f'/delete_category/{category.id}', follow_redirects=True)

    assert response.status_code == 200
    assert b'Category deleted successfully!' in response.data

    # Check if category was removed
    with client.application.app_context():
        deleted_category = Category.query.get(category.id)
        assert deleted_category is None
