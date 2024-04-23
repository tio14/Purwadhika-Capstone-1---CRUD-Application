import os
import Database as db
from tabulate import tabulate as tb
import time

def input_y_n(text):
    while True:
        cont = input(text).lower()
        if cont in ["y", "n"]:
            break
        print("Please input y/n!\n")
    return cont

def input_number(text = "Enter the corresponding number : ", required=True):
    while True:
        user_input = input(text)
        # For blank value input
        if required == False:
            if user_input == "":
                return user_input
        if user_input.isdigit():
            break
        print('Please input a "number"!\n')
    return int(user_input)

def input_number_max(text, max_value):
    while True:                                                 
        user_input = input_number(text)                         
        if user_input == 0:
            print("Number can't be 0!\n")
        elif user_input > max_value:
            print("Exceed the maximum number!\n")
        else:
            break
    return user_input

def input_name(text, required=True):
    while True:
        user_input = input(text).title()
        # For blank value input
        if required == False:
            if user_input == "":
                return user_input
        if user_input == "":
            print("Value can't be a blank!")
        elif user_input in db.products["Name"]:
            print("This name already exist!\n")
        else:
            break
    return user_input    

def banner():
    os.system('cls')
    print("""\t\tTokoIndo
========================================""")

def tabulate_view(data):
    print(tb(data, headers='keys', tablefmt='grid'), end="\n\n") 

def product_details(index):
    print(f"""Name\t: {db.products["Name"][index-1]}
Stock\t: {db.products["Stock"][index-1]}
Price\t: {db.products["Price"][index-1]}\n""")
    
def cart_details(index):
    print(f"""Name\t\t: {db.carts["Name"][index-1]}
Quantity\t: {db.carts["Quantity"][index-1]}
Price/unit\t: {db.carts["Price/unit"][index-1]}\n""")    

def check_products_stock():
    banner()
    print("\t   Our product list\n")
    tabulate_view(db.carts)
    carts_name = db.carts["Name"]
    for name in carts_name:
        cart_index = db.carts["Name"].index(name)
        if name not in db.products["Name"]:
            print(f'"{name}" is out of stock!')
            print(f'Deleting {name} from the carts...\n')
            delete_item(db.carts, cart_index)
            time.sleep(2)
        else:
            product_index = db.products["Name"].index(name)
            quantity = db.carts["Quantity"][cart_index]
            stock = db.products["Stock"][product_index]
            if stock < quantity:
                print(f'"{name}" is understocked!')
                print(f'{quantity} in your carts, {stock} available! Resizing...\n')
                db.carts["Quantity"][cart_index] = db.products["Stock"][product_index]
                time.sleep(2)

def add_product_to_carts():
    while True:
        banner()
        print("\t   Our product list\n")
        tabulate_view(db.products)
        while True:
            index = input_number_max("Enter the index of product you want to add to your carts : ",
                                     max(db.products["Index"]))
            if db.products["Stock"][index-1] == 0:
                print(f'{db.products["Name"][index-1]} is out of stock!\n')
            else: 
                break
        banner()
        print("\tPurchase this product\n")
        product_details(index)
        product_stock = db.products["Stock"][index-1]
        if db.products["Name"][index-1] in db.carts["Name"]:
            product_name = db.products["Name"][index-1]
            carts_index = db.carts["Name"].index(product_name)
            cart_prod_qty = db.carts["Quantity"][carts_index]
            print(f'You already put "{cart_prod_qty}" in your cart\n')
            if cart_prod_qty == product_stock:
                print('You already have a maximum number of stock from this product in your carts!\n')
                time.sleep(5)
                break
            else:
                quantity = input_number_max("Enter the amount : ",
                                            product_stock - cart_prod_qty)
                db.carts["Quantity"][carts_index] += quantity
                db.carts["Price"][carts_index] += db.products["Price"][index-1] * quantity
        else:
            quantity = input_number_max("Enter the amount : ",
                                        product_stock)
            db.carts["Name"].append(db.products["Name"][index-1])
            db.carts["Quantity"].append(quantity)
            db.carts["Price/unit"].append(db.products["Price"][index-1])
            db.carts["Price"].append(db.products["Price"][index-1] * quantity)
            if len(db.carts["Index"]) == 0:
                db.carts["Index"].append(1)
            else:    
                db.carts["Index"].append(db.carts["Index"][-1] + 1)
        # Carts List
        banner()
        print("\t\tYour Carts\n")
        tabulate_view(db.carts)
        cont = input_y_n("Do you want to adda another product? (y/n) = ")
        if cont == "n":
            break

def update_item_carts():
    if len(db.carts["Index"]) > 0:
        banner()
        print("\t   Your current cart\n")
        tabulate_view(db.carts)
        index = input_number_max("Enter the index of product you want to update : ",
                                 max(db.carts["Index"]))
        banner()
        print("\tUpdate this product in carts\n")
        cart_details(index)
        product_name = db.carts["Name"][index-1]
        index_in_products = db.products["Name"].index(product_name)
        print(f"Stock\t: {db.products['Stock'][index_in_products]}\n")
        print("Change into (enter the same number if you don't want to change)")
        quantity = input_number_max("Enter the amount : ",
                                    db.products['Stock'][index_in_products])
        db.carts["Quantity"][index-1] = quantity
    else:
        print("There's no product in carts!\n")
        time.sleep(2)

def delete_item_carts():
    if len(db.carts["Index"]) > 0:
        banner()
        print("\t   Your current cart\n")
        tabulate_view(db.carts)
        index = input_number_max("Enter the index of product you want to delete : ",
                                 max(db.carts["Index"]))
        cont = input_y_n(f'Delete "{db.carts["Name"][index-1]}" from your product list? (y/n) = ').lower()
        if cont == "y":
            delete_item(db.carts, index-1)
        else:
            print("Cancelled!")
            time.sleep(2)
    else:
        print("There's no product in carts!\n")
        time.sleep(2)

def delete_item(data, index):
    for key in data:
        del data[key][index]
    data["Index"].clear()
    data["Index"].extend(i for i in range(1, len(data['Name'])+1))    

def checkout_carts():
    if len(db.carts["Index"]) > 0:
        banner()
        print("\t   Your current carts\n")
        tabulate_view(db.carts)
        total_price = 0
        for price in db.carts["Price"]:
            total_price += price
        print(f"\nTotal price\t\t\t= {total_price:,d}")
        while True:
            cash = input_number("Enter the amount of cash\t= ")
            if cash >= total_price:
                break    
            print(f"The cash wasn't enough. You need to add {total_price - cash:,d} more\n")
        # Substract stock in products
        for cart_index in range(len(db.carts["Index"])):
            name = db.carts["Name"][cart_index]
            product_index = db.products["Name"].index(name)
            db.products["Stock"][product_index] -= db.carts["Quantity"][cart_index]
        # Delete all item in carts
        for key in db.carts:
            db.carts[key].clear()
        print("\nThank You!!!")
        if cash > total_price:
            print(f"Here is your change : {cash - total_price:,d}")
        time.sleep(2)
    else:
        print("There's no product in carts!\n")
        time.sleep(2)

def add_new_product():
    banner()
    name = input_name("\nProduct Name\t: ")
    stock = input_number("Stock\t\t: ")
    price = input_number("Price\t\t: ")
    db.products["Index"].append(max(db.products["Index"]) + 1)
    db.products["Name"].append(name)
    db.products["Stock"].append(stock)
    db.products["Price"].append(price)

def update_product():
    banner()
    print("\t   Your product list\n")
    tabulate_view(db.products)
    index = input_number_max("Enter the index of product you want to update : ", max(db.products["Index"]))
    
    banner()
    print("\tUpdate current product\n")
    product_details(index)
    print("Change into (enter blank value if you don't want to change certain product property)")
    prev_name = db.products["Name"][index-1]
    name = input_name("Name\t: ", required=False)
    stock = input_number("Stock\t: ", required=False)
    price = input_number("Price\t: ", required=False)
    name = update_product_if_empty("Name", name, index)
    stock = update_product_if_empty("Stock", stock, index)
    price = update_product_if_empty("Price", price, index)
    if prev_name in db.carts["Name"]:
        cart_index = db.carts["Name"].index(prev_name)
        db.carts["Name"][cart_index] = name
        db.carts["Price/unit"][cart_index] = price
        db.carts["Price"][cart_index] = price * db.carts["Quantity"][cart_index]

def update_product_if_empty(property_name, new_value, index):
    if new_value == "":
        new_value = db.products[property_name][index-1]
    else:
        db.products[property_name][index-1] = new_value
    return new_value

def delete_product():
    banner()
    print("\t   Your product list\n")
    tabulate_view(db.products)
    index = input_number_max("Enter the index of product you want to delete : ",
                             max(db.products["Index"]))
    cont = input_y_n(f'\nDelete "{db.products["Name"][index-1]}" from your product list? (y/n) = ').lower()
    if cont == "y":
        for key in db.products:
            del db.products[key][index-1]
        db.products["Index"].clear()
        db.products["Index"].extend(i for i in range(1, len(db.products['Name'])+1))
    else:
        print("Cancelled!")
        time.sleep(2)

def login():
    # Choose user type 
    banner()
    print("""\t\tLog-In\n
Enter as a :
1. Consumer
2. Seller
. Exit\n""")
    user_type_number = input_number()
    if user_type_number in [1,2]:
        user_type_db = db.consumers if user_type_number==1 else db.sellers
        user_type_string = "Consumer" if user_type_number==1 else "Seller"
        os.system('cls')
        # Enter email and password
        banner()
        print(f"\t    {user_type_string} Log-In\n")
        while True:
            login_id = input("Phone Number or Email\t: ").lower()
            if login_id in user_type_db['Phone Number']:
                access_type = 'Phone Number'
                break
            elif login_id in user_type_db['Email']:
                access_type = 'Email'
                break
            print('Phone Number/Email not registered!\n')
        while True:
            user_index = user_type_db[access_type].index(login_id)
            login_pass = input("Enter your password\t: ")
            if login_pass == user_type_db['Password'][user_index]:
                break
            print('Incorrect Password!\n') 
    return user_type_number

def consumer_menu():
    if len(db.carts["Index"]) > 0:
        check_products_stock()
    while True:
        banner()
        print("\t   Your current carts\n")
        tabulate_view(db.carts)
        print("""Welcome dear customer
List Menu :
1. Add Product to Carts
2. Update Product in Carts
3. Delete Product in Carts
4. Checkout
. Log-Out\n""")
        menu_number = input_number()
        if menu_number == 1:
            add_product_to_carts()
        elif menu_number == 2:
            update_item_carts()
        elif menu_number == 3:
            delete_item_carts()
        elif menu_number == 4:
            checkout_carts()
        else:   
            break

def seller_menu():
    while True:
        banner()
        print("\t   Your product list\n")
        tabulate_view(db.products)
        print("""List Menu :
1. Add New Product  
2. Update Product
3. Delete a Product
. Log-Out\n""")
        menu_number = input_number()
        if menu_number == 1:
            add_new_product()
        elif menu_number == 2:
            update_product()
        elif menu_number == 3:
            delete_product()
        else:   
            break

while True:
    user_type_number = login()
    if user_type_number == 1:
        consumer_menu()
    elif user_type_number == 2:
        seller_menu()
    else:
        break