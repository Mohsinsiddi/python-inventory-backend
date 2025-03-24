class Category:
    """Encapsulated Category class"""

    def __init__(self, name, description):
        self.__name = name
        self.__description = description

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def __str__(self):
        return f'{self.__name}: {self.__description}'
