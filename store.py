import products


class Store:
    """
    Represents a store containing a list of products.

    Attributes:
        products (list[products.Product]): A list of products available in the store.
    """

    def __init__(self, products_list: list[products.Product]):
        """
        Initializes the Store with a list of products.

        Args:
            products_list (list[products.Product]): A list of Product instances.

        Raises:
            TypeError: If products_list is not a list or contains non-Product elements.
        """
        # Check if products_list is a list
        if not isinstance(products_list, list):
            raise TypeError("products_list must be a list of Product objects.")
        # Check if all elements are instances of Product
        if not all(isinstance(product, products.Product) for product in products_list):
            raise TypeError("All elements in products_list must be instances of the Product class.")

        self.products = products_list

    def __contains__(self, item):
        return item in self.products

    def __add__(self, other):
        # store validation
        if not isinstance(other, Store):
            raise TypeError("Can only add another Store.")

        new_store = Store(self.products.copy())

        for product in other.products:
            new_store.add_product(product)

        return new_store

    def add_product(self, product):
        """
        Adds a new product to the store.
        If product already exists, update the quantity

        Args:
            product (products.Product): The product to be added.

        Raises:
            TypeError: If the provided product is not an instance of the Product class.

        Returns:
            str: A confirmation message indicating successful addition.
        """
        # Product validation
        if not isinstance(product, products.Product):
            raise TypeError("product must be instance of the Product class.")

        if product in self.products:
            product_index = self.products.index(product)
            self.products[product_index].quantity += product.quantity
            return f"Product '{product.name}' is already in the store. Quantity was updated."

        self.products.append(product)
        return f"Product '{product.name}' added successfully."

    def remove_product(self, product):
        """
        Removes a product from the store.

        Args:
            product (products.Product): The product to be removed.

        Raises:
            TypeError: If the provided product is not an instance of the Product class.
            ValueError: If the product does not exist in the store.

        Returns:
            str: A confirmation message indicating successful removal.
        """
        # Product validation
        if not isinstance(product, products.Product):
            raise TypeError("product must be instance of the Product class.")
        if not product in self.products:
            raise ValueError("Product doesn't exist.")

        self.products.remove(product)
        return f"Product '{product.name}' removed successfully."

    def get_total_quantity(self) -> int:
        """
        Calculates the total quantity of all products in the store.

        Returns:
            int: The total quantity of all products.
        """
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> list[products.Product]:
        """
        Retrieves all active products from the store.

        Returns:
            list[products.Product]: A list of active Product instances.
        """
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list: list[tuple]):
        """
        Processes an order based on the given shopping list.

        Args:
            shopping_list (list[tuple]): A list of tuples where each tuple contains a Product instance
                                         and an integer representing the quantity.

        Raises:
            TypeError: If shopping_list is not a list or if any item is not a tuple of (Product, int).
            ValueError: If a product is not available in the store or if quantity is negative.

        Returns:
            float: The total price of the order.
        """
        # Ensure shopping_list is a list
        if not isinstance(shopping_list, list):
            raise TypeError("shopping_list must be a list of tuples (Product, int).")

        total_order_price = 0

        for item in shopping_list:
            # Ensure each item is a tuple with exactly two elements
            if not isinstance(item, tuple) or len(item) != 2:
                raise TypeError("Each item in shopping_list must be a tuple (Product, int).")

            product, quantity = item  # Unpack the tuple

            # Ensure the product exists in the store
            if product not in self.products:
                raise ValueError(f"Product {product.name} is not available in the store.")

            # Ensure the first element is a Product instance
            if not isinstance(product, products.Product):
                raise TypeError("First item in tuple must be a Product instance.")

            # Ensure the second element is an integer representing quantity
            if not isinstance(quantity, int):
                raise TypeError("Quantity must be an integer.")
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")

            # Process the purchase and update total price
            total_order_price += product.buy(quantity)

        return total_order_price
