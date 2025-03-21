CURRENCY = "€"


class Product:
    """
    Represents a product with a name, price, and quantity.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product.
        active (bool): Indicates whether the product is active.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a Product instance with validation.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            quantity (int): The initial quantity of the product.

        Raises:
            TypeError: If name is not a string, price is not a number, or quantity is not an integer.
            ValueError: If name is empty, price is negative, or quantity is negative.
        """
        # Name validation
        if not isinstance(name, str):
            raise TypeError("Product name must be a string.")
        if not name.strip():
            raise ValueError("Product name cannot be empty or just spaces.")

        # Price validation
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number (int or float).")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        # Instance Variables
        self.name = name
        self.price = float(price)
        self.quantity = quantity
        self.active = True

    # Methods
    def get_quantity(self) -> int:
        """
        Retrieves the current quantity of the product.

        Returns:
            int: The current quantity of the product.
        """
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Sets the quantity of the product.

        Args:
            quantity (int): The new quantity to set.

        Raises:
            TypeError: If quantity is not an integer.
            ValueError: If quantity is negative.
        """
        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Checks if the product is active.

        Returns:
            bool: True if the product is active, False otherwise.
        """
        return self.active

    def activate(self):
        """
        Activates the product by setting its active status to True.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivates the product by setting its active status to False.
        """
        self.active = False

    def show(self) -> str:
        """
        Displays product details in a formatted string.

        Returns:
            str: A formatted string showing product name, price, and quantity.
        """
        return f"{self.name} | Price: {self.price}{CURRENCY} | Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        """
        Processes the purchase of a specified quantity of the product.

        Args:
            quantity (int): The number of units to buy.

        Raises:
            TypeError: If quantity is not an integer.
            ValueError: If quantity is negative or exceeds available stock.

        Returns:
            float: The total price of the purchased products, rounded to two decimal places.
        """
        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if self.quantity >= quantity:
            updated_quantity = self.quantity - quantity
            self.set_quantity(updated_quantity)
            return round(float(quantity * self.price), 2)
        raise ValueError("Not enough products in stock.")
