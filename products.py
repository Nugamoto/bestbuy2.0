import promotions

CURRENCY = "€"


class Product:
    """
    Represents a product with a name, price, and quantity.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product.
        active (bool): Indicates whether the product is active.
        promotion (promotions.Promotion or None): The promotion applied to the product.
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
        self._quantity = quantity
        self.active = True
        self._promotion = None

    @property
    def promotion(self):
        """Returns the current promotion applied to the product, if any."""
        return self._promotion

    @promotion.setter
    def promotion(self, value):
        """Sets the promotion for the product.

        Args:
            value (promotions.Promotion or None): The promotion to apply, or None.

        Raises:
            TypeError: If value is not an instance of promotions.Promotion or None.
        """
        if value is not None and not isinstance(value, promotions.Promotion):
            raise TypeError("Promotion must be an instance of promotions.Promotion or None.")
        self._promotion = value

    @property
    def quantity(self):
        """Gets the current quantity of the product."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Sets the quantity of the product. If quantity is set to 0, the product is deactivated.

        Args:
            value (int): The new quantity to set.

        Raises:
            TypeError: If value is not an integer.
            ValueError: If value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("Quantity must be an integer.")
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value
        if self._quantity == 0:
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
        if quantity <= 0:
            raise ValueError("Quantity cannot be negative or 0.")

        if self.quantity >= quantity:
            updated_quantity = self.quantity - quantity
            self.quantity = updated_quantity
            if self.promotion is not None:
                total_price = self.promotion.apply_promotion(self, quantity)
            else:
                total_price = float(quantity * self.price)
            return round(total_price, 2)
        raise ValueError("Not enough products in stock.")

    def __str__(self):
        """
        Displays product details in a formatted string.

        Returns:
            str: A formatted string showing product name, price, quantity and Promotion.
        """
        promotion_str = f" | Promotion: {self.promotion.name}" if self.promotion is not None else ""
        return (f"{self.name} | Price: {self.price}{CURRENCY} | "
                f"Quantity: {self.quantity}{promotion_str}")

    def __gt__(self, other):
        """
        Compare if this product's price is greater than another product's price.

        Args:
            other (Product): The product to compare against.

        Returns:
            bool: True if this product's price is greater, False otherwise.
        """
        return self.price > other.price

    def __lt__(self, other):
        """
        Compare if this product's price is less than another product's price.

        Args:
            other (Product): The product to compare against.

        Returns:
            bool: True if this product's price is less, False otherwise.
        """
        return self.price < other.price

    def __eq__(self, other):
        """
        Check if two products are equal based on their name.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: True if the other object is a Product and has the same name, False otherwise.
        """
        if not isinstance(other, Product):
            return False
        return self.name == other.name


class NonStockedProduct(Product):
    """
    Represents a product that does not have a quantity in stock.
    It is intended for non-physical products, such as software licenses.

    Inherits from Product, but always fixes quantity to 0.
    """

    def __init__(self, name: str, price: float):
        """
        Initialize a NonStockedProduct.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
        """
        super().__init__(name, price, 0)

    def __str__(self):
        """
        Return a string representation of the product.

        Returns:
            str: A formatted string showing product name, price and Promotion.
        """
        promotion_str = f" | Promotion: {self.promotion.name}" if self.promotion is not None else ""
        return (f"{self.name} | Price: {self.price}{CURRENCY} | "
                f"Quantity: Unlimited"
                f"{promotion_str}")

    def is_active(self) -> bool:
        """
        Indicates that NonStockedProduct instances are always considered active.

        Returns:
            bool: Always returns True, since non-stocked products do not depend
                  on quantity for their availability.
        """
        return True

    def buy(self, quantity: int) -> float:
        """
        Process the purchase of a specified quantity of the product.

        Args:
            quantity (int): The number of units to buy.

        Raises:
            TypeError: If quantity is not an integer.
            ValueError: If quantity is negative or zero.

        Returns:
            float: The total price of the purchased products, rounded to two
                   decimal places.
        """
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("Quantity cannot be negative or 0.")

        if self.promotion is not None:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        return round(float(total_price), 2)


class LimitedProduct(Product):
    """
    Class representing a product with a purchase limit.

    This class extends the Product class by adding a maximum purchase limit
    per transaction.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initialize a new LimitedProduct instance.

        Parameters:
            name (str): The name of the product.
            price (float): The price of the product.
            quantity (int): The available quantity in stock.
            maximum (int): The maximum number of items that can be purchased in one transaction.

        Raises:
            TypeError: If maximum is not an integer.
            ValueError: If maximum is not positive.
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    @property
    def maximum(self) -> int:
        """
        Get the maximum allowed quantity per purchase.

        Returns:
            int: The maximum number of items that can be purchased.
        """
        return self._maximum

    @maximum.setter
    def maximum(self, value: int):
        """
        Set the maximum allowed quantity per purchase.

        Parameters:
            value (int): The new maximum value.

        Raises:
            TypeError: If value is not an integer.
            ValueError: If value is less than or equal to 0.
        """
        if not isinstance(value, int):
            raise TypeError("Maximum must be an integer.")
        if value <= 0:
            raise ValueError("Maximum must be positive.")
        self._maximum = value

    def __str__(self):
        """
        Return a string representation of the product.

        The string includes the product's name, price, available quantity,
        and maximum allowed purchase quantity.

        Returns:
            str: A formatted string with the product details.
        """
        promotion_str = f" | Promotion: {self.promotion.name}" if self.promotion is not None else ""
        return (f"{self.name} | "
                f"Price: {self.price}{CURRENCY} | "
                f"Quantity: {self.quantity} | "
                f"Maximum: {self.maximum}"
                f"{promotion_str}")

    def buy(self, quantity: int) -> float:
        """
        Attempt to purchase a specified quantity of the product.

        Validates that the quantity is an integer, positive, does not exceed the
        maximum allowed per transaction, and that there is enough stock available.
        If valid, updates the stock and returns the total price for the purchase.

        Parameters:
            quantity (int): The number of items to purchase.

        Returns:
            float: The total price for the purchased items, rounded to 2 decimal places.

        Raises:
            TypeError: If quantity is not an integer.
            ValueError: If quantity is less than or equal to 0.
            ValueError: If quantity exceeds the maximum allowed per transaction.
            ValueError: If there is insufficient stock available.
        """
        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("Quantity cannot be negative or 0.")

        # Maximum validation
        if quantity > self.maximum:
            raise ValueError(f"You cannot buy more than "
                             f"'{self.maximum}' pcs from '{self.name}'.")

        if self.quantity >= quantity:
            updated_quantity = self.quantity - quantity
            self.quantity = updated_quantity
            if self.promotion is not None:
                total_price = self.promotion.apply_promotion(self, quantity)
            else:
                total_price = quantity * self.price

            return round(float(total_price), 2)

        raise ValueError("Not enough products in stock.")
