from modules.SuperCashier import *

# A flag sign program is running
super_cashier_running = True

# Create new instance of SuperCashier class
sc = SuperCashier()

# Customer create Transaction ID
sc.transaction()

while super_cashier_running:
    # Show all menu
    sc.menus()

    # Access attribute class
    user_option = sc.user_option

    # Branching menu
    if user_option == 0:
        print("> Pilihan menu yang anda masukkan tidak tersedia!")
    elif user_option == 1:
        # Customer menambah item
        sc.add_item()
    elif user_option == 2:
        # Customer mengubah nama item
        sc.update_item_name()
    elif user_option == 3:
        # Customer mengubah jumlah item
        sc.update_item_qty()
    elif user_option == 4:
        # Customer mengubah harga item
        sc.update_item_price()
    elif user_option == 5:
        # Customer menghapus item
        sc.delete_item()
    elif user_option == 6:
        # Customer reset transaksi
        sc.reset_transaction()
    elif user_option == 7:
        # Customer cek order
        sc.check_order()
    else:
        sc.check_out()
        super_cashier_running = False
