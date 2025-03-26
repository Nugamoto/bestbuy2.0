import pytest

from products import Product


def test_create_valid_product():
    product = Product("Test product", 99, 5)
    assert isinstance(product, Product)
    assert product.name == "Test product"
    assert product.price == 99
    assert product.quantity == 5


def test_create_invalid_product():
    with pytest.raises(TypeError, match="Product name must be a string"):
        Product(23, 99, 5)

    with pytest.raises(TypeError, match="Price must be a number"):
        Product("Test product", "99", 5)

    with pytest.raises(TypeError, match="Quantity must be an integer"):
        Product("Test product", 99, [5, 10])

    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product("", 99, 5)

    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("Test product", -99, 5)

    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        Product("Test product", 99, -5)


def test_product_becomes_inactive():
    product = Product("Test product", 99, 5)
    assert product.is_active() is True

    product.set_quantity(0)

    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_buy_product():
    product = Product("Test product", 100, 5)

    assert product.buy(3) == 300.00
    assert product.get_quantity() == 2

    assert product.buy(2) == 200.00
    assert product.get_quantity() == 0
    assert product.is_active() is False

    with pytest.raises(ValueError, match="Quantity cannot be negative or 0."):
        product.buy(0)

    with pytest.raises(ValueError, match="Quantity cannot be negative or 0."):
        product.buy(-5)



def test_buy_product_too_large_quantity():
    product = Product("Test product", 100, 5)
    with pytest.raises(ValueError, match="Not enough products in stock"):
        product.buy(10)
