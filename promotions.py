from abc import ABC, abstractmethod

import products


class Promotion(ABC):
    """
    Abstract base class for promotions.

    Attributes:
        name (str): The name of the promotion.

    Methods:
        apply_promotion(product, quantity) -> float:
            Abstract method to apply the promotion to a product purchase.
    """

    def __init__(self, name):
        # Name validation
        if not isinstance(name, str):
            raise TypeError("Promotion name must be a string.")
        if not name.strip():
            raise ValueError("Promotion name cannot be empty or just spaces.")

        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the promotion to the given product and quantity.

        Parameters:
            product (products.Product): The product instance to which the promotion applies.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The total price after applying the promotion.
        """
        pass


class PercentDiscount(Promotion):
    """
    Promotion that applies a percentage discount to the total price.

    Attributes:
        percent (float): The discount percentage (greater than 0 and less than 100).
    """

    def __init__(self, name, percent):
        """
        Initialize a PercentDiscount promotion.

        Parameters:
            name (str): The name of the promotion.
            percent (int or float): The discount percentage.

        Raises:
            TypeError: If the name is not a string or percent is not a number.
            ValueError: If the name is empty or percent is not between 0 and 100.
        """
        super().__init__(name)
        # percent validation
        if not isinstance(percent, (int, float)):
            raise TypeError("Percent must be an integer or float")
        if not 0 < percent < 100:
            raise ValueError("Percent must be greater than 0 and less than 100.")

        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Calculate the price after applying the percentage discount.

        Parameters:
            product (products.Product): The product instance.
            quantity (int): The number of products purchased.

        Returns:
            float: The discounted total price.

        Raises:
            TypeError: If product is not an instance of products.Product or quantity is not an integer.
            ValueError: If quantity is negative.
        """
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
    """
    Promotion that applies a second item at half price.

    This promotion calculates the total price such that for every pair of items,
    the second item is sold at half its normal price.
    """

    def __init__(self, name):
        """
        Initialize a SecondHalfPrice promotion.

        Parameters:
            name (str): The name of the promotion.

        Raises:
            TypeError: If the name is not a string.
            ValueError: If the name is empty.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Calculate the total price with every second product at half price.

        Parameters:
            product (products.Product): The product instance.
            quantity (int): The number of products purchased.

        Returns:
            float: The total price after applying the promotion.

        Raises:
            TypeError: If product is not an instance of products.Product or quantity is not an integer.
            ValueError: If quantity is negative.
        """
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
    """
    Promotion that implements a "buy 2, get 1 free" offer.

    For every three products purchased, the customer pays for two.
    """

    def __init__(self, name):
        """
        Initialize a ThirdOneFree promotion.

        Parameters:
            name (str): The name of the promotion.

        Raises:
            TypeError: If the name is not a string.
            ValueError: If the name is empty.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Calculate the total price applying the "buy 2, get 1 free" promotion.

        For every three products, the customer pays for two.

        Parameters:
            product (products.Product): The product instance.
            quantity (int): The number of products purchased.

        Returns:
            float: The total price after applying the promotion.

        Raises:
            TypeError: If product is not an instance of products.Product or quantity is not an integer.
            ValueError: If quantity is negative.
        """
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
