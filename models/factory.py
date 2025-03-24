from models.product import Product
from models.category import Category


class ProductFactory:
    """Factory for creating products"""

    @staticmethod
    def create_product(product_id, name, price, quantity, category_id):
        return Product(product_id, name, price, quantity, category_id)


class CategoryFactory:
    """Factory for creating categories"""

    @staticmethod
    def create_category(name, description):
        return Category(name, description)
