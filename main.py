import products
import store
from console import enter_to_continue, get_valid_number_from_user, display_products, display_menu, \
    display_total_quantity, order_process

# setup initial stock of inventory
product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                products.Product("Google Pixel 7", price=500, quantity=250)
                ]


def main():
    """
    Main function to run the store application.

    Initializes the store and provides a menu for user interaction.
    The user can view products, check total quantity, process orders,
    or exit the application.
    """
    best_buy = store.Store(product_list)
    while True:
        display_menu()
        user_input = get_valid_number_from_user(1, 4)

        match user_input:
            case 1:
                display_products(best_buy)
                enter_to_continue()
            case 2:
                display_total_quantity(best_buy)
                enter_to_continue()
            case 3:
                order_process(best_buy)
                enter_to_continue()
            case 4:
                break


if __name__ == "__main__":
    main()
