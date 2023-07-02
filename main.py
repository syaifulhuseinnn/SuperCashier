from modules.SuperCashier import *

# A flag sign program is running
super_cashier_is_running = True

# Create new instance of SuperCashier class
sc = SuperCashier()

# Customer create Transaction ID
sc.transaction()

while super_cashier_is_running:
    # Show all menu
    sc.menus()

    # Access 'user_option' attribute class
    user_option = sc.user_option

    # Branching menu
    if user_option == 0:
        print("> Pilihan menu yang anda masukkan tidak tersedia!")
    elif user_option == 1:
        # Customer add item
        item_name = input("Masukkan nama item: ")
        item_quantity = input("Masukkan jumlah item: ")
        item_price = input("Masukkan harga item: ")

        sc.add_item(item_name, item_quantity, item_price)
    elif user_option == 2:
        # Customer update item name
        old_item_name = input("Masukkan nama item yang ingin diubah: ")
        new_item_name = input("Masukkan nama item yang baru: ")

        sc.update_item_name(old_item_name, new_item_name)
    elif user_option == 3:
        # Customer update item quantity
        item_name = input("Masukkan nama item yang ingin diubah jumlahnya: ")
        new_item_qty = input("Masukkan jumlah item yang baru: ")

        sc.update_item_qty(item_name, new_item_qty)
    elif user_option == 4:
        # Customer update item price
        item_name = input("Masukkan nama item yang ingin diubah harganya: ")
        new_item_price = input("Masukkan harga item yang baru: ")

        sc.update_item_price(item_name, new_item_price)
    elif user_option == 5:
        # Customer menghapus item
        item_name = input("Masukkan nama item yang ingin dihapus: ")

        sc.delete_item(item_name)
    elif user_option == 6:
        # Customer reset transaksi
        sc.reset_transaction()
    elif user_option == 7:
        # Customer cek order
        sc.check_order()
    else:
        check_out = sc.check_out()
        if check_out is not False:
            super_cashier_is_running = False
