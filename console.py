from products import CURRENCY


def enter_to_continue():
    """
    Prompts the user to press 'Enter' to continue.
    """
    input("\nPress 'Enter' to continue")


def get_valid_number_from_user(start_num: int, end_num: int) -> int:
    """
    Gets a valid number from the user within a specified range.

    Args:
        start_num (int): The starting number of the valid range.
        end_num (int): The ending number of the valid range.

    Returns:
        int: The valid number chosen by the user or 0 if input is empty.
    """
    while True:
        user_input = input(f"Please choose a number({start_num}-{end_num}): ")
        if not user_input:
            return None
        if not user_input.isdigit():
            print("You haven't entered a number!")
            continue
        if not start_num <= int(user_input) <= end_num:
            print(f"Number must between '{start_num}' and '{end_num}'!")
            continue
        return int(user_input)


def display_menu():
    """
    Displays the store menu with available options.
    """
    print(f"\n\n\t--- Store Menu ---\n"
          f"\t------------------\n"
          f"1. List all products in store\n"
          f"2. Show total amount in store\n"
          f"3. Make an order\n"
          f"4. Quit\n")


def display_products(store_obj):
    """
    Displays all active products in the store.

    Args:
        store_obj: The store object containing the product list.
    """
    products_list = store_obj.get_all_products()
    if not products_list:
        print("\nStore is sold out.")
    else:
        print(f"\nAll Products:\n"
              f"------------")
        for num, product in enumerate(products_list, 1):
            print(f"{num}. {product.show()}")
        print(f"------------")


def display_total_quantity(store_obj):
    """
    Displays the total quantity of all products in the store.

    Args:
        store_obj: The store object containing all products.
    """
    print(f"\nTotal of '{store_obj.get_total_quantity()}' items in store.")


def order_process(store_obj):
    """
    Handles the order process, allowing users to select and purchase products.

    Args:
        store_obj: The store object containing all products.
    """
    order_list = []
    products_list = store_obj.get_all_products()
    display_products(store_obj)
    current_quantities = [product.get_quantity() for product in products_list]
    while True:
        print(f"When you want to finish order, enter empty text.\n"
              f"Which product do you want?")
        user_input = get_valid_number_from_user(1, len(products_list))
        if not user_input:
            if order_list:
                total_order = store_obj.order(order_list)
                print(f"\n*** Order made. Total payment: {total_order}{CURRENCY} ***")
                break
            print("\nOrder was empty.")
            break

        current_product_idx = user_input - 1
        if current_quantities[current_product_idx] < 1:
            print("\nYou have all items in you cart.\n"
                  "Checkout or add another product.\n")
            continue
        current_product = products_list[current_product_idx]
        print(f"What amount do you want?")
        quantity = get_valid_number_from_user(1, current_quantities[current_product_idx])
        if quantity:
            order_list.append((current_product, quantity))
            current_quantities[current_product_idx] -= quantity
            print(f"\n'{current_product.name}' successfully added to cart. ({quantity} pcs)\n")
