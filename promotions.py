from abc import ABC, abstractmethod

import products


class Promotion(ABC):  # ABC steht für Abstract Base Class
    def __init__(self, name):
        # Name validation
        if not isinstance(name, str):
            raise TypeError("Promotion name must be a string.")
        if not name.strip():
            raise ValueError("Promotion name cannot be empty or just spaces.")

        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        # percent validation
        if not isinstance(percent, (int, float)):
            raise TypeError("Percent must be an integer or float")
        if not 0 < percent < 100:
            raise ValueError("Percent must be greater than 0 and less than 100.")

        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        # product validation
        if not isinstance(product, products.Product):
            raise TypeError(f"{product} is not from the Product class.")

        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount


class SecondHalfPrice(Promotion):
    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        # product validation
        if not isinstance(product, products.Product):
            raise TypeError(f"{product} is not from the Product class.")

        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return (full_price_items * product.price) + (half_price_items * product.price * 0.5)


class ThirdOneFree(Promotion):
    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        # product validation
        if not isinstance(product, products.Product):
            raise TypeError(f"{product} is not from the Product class.")

        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        sets_of_three = quantity // 3
        remaining = quantity % 3
        payable_quantity = (sets_of_three * 2) + remaining
        return payable_quantity * product.price
