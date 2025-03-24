class Product:
    """Encapsulated Product class with factory pattern"""

    def __init__(self, product_id, name, price, quantity, category_id):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__category_id = category_id

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def get_category_id(self):
        return self.__category_id

    def __str__(self):
        return f'{self.__name} (${self.__price}), Qty: {self.__quantity}'

