CURRENCY = "€"


class Product:
    def __init__(self, name: str, price: float, quantity: int):
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
        return self.quantity

    def set_quantity(self, quantity: int):
        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self) -> str:
        return f"{self.name} | Price: {self.price}{CURRENCY} | Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        # Quantity validation
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if self.quantity >= quantity:
            updated_quantity = self.quantity - quantity
            self.set_quantity(updated_quantity)
            return round(float(quantity * self.price), 2)
        else:
            raise ValueError("Not enough products in stock.")
