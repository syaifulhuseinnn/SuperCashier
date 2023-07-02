# A library change Dictionary to JSON format
import json
import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable
from helpers.helpers import *


class SuperCashier:
    def __init__(self):
        """
        Initializes a new instance of the SuperCashier class.
        """
        self.transaction_id = ""
        self.items = []
        self.order = []
        self.user_option = 0
        self.grand_total = 0

    def check_discount(self, total_price):
        """
        Checks if a discount is applicable based on the total price.

        Args:
            total_price (int): The total price of the items.

        Returns:
            dict or bool: A dictionary containing the discount and the total
            price after discount, or False if no discount is applicable.
        """
        if total_price > 200_000 and total_price <= 300_000:
            discount = total_price * (5/100)
            total = total_price - discount
            return {"discount": int(discount), "total": int(total)}
        elif total_price > 300_000 and total_price <= 500_000:
            discount = total_price * (6/100)
            total = total_price - discount
            return {"discount": int(discount), "total": int(total)}
        elif total_price > 500_000:
            discount = total_price * (7/100)
            total = total_price - discount
            return {"discount": int(discount), "total": int(total)}
        else:
            return False

    def insert_to_table(self):
        """
        Inserts the transaction details into the database.
        """

        # Convert list of dictionary to list of tuple
        records = []
        for i in range(len(self.order)):
            records.append(
                (None,
                 self.order[i]["item_name"],
                 self.order[i]["item_quantity"],
                 self.order[i]["item_price"],
                 self.order[i]["total_price"],
                 self.order[i]["discount"],
                 self.order[i]["price_after_discount"],)
            )

        # Create connection
        conn = None

        try:
            conn = sqlite3.connect('./database/SuperCashier.db')
        except Error as e:
            print(e)

        query_create_table_transaction = """
        CREATE TABLE IF NOT EXISTS transactions
        (
            no_id INTEGER PRIMARY KEY,
            nama_item TEXT NOT NULL,
            jumlah_item INT NOT NULL,
            harga INT NOT NULL,
            total_harga INT NOT NULL,
            diskon INT NULL,
            harga_diskon INT NULL
        );
        """

        query_insert_records = """
        INSERT INTO transactions
        VALUES (?,?,?,?,?,?,?);
        """

        try:
            c = conn.cursor()
            c.execute(query_create_table_transaction)
            c.executemany(query_insert_records, records)
            print("Info: Detail transaksi telah disimpan ke database!")
        except Error as e:
            print(e)

        conn.commit()
        conn.close()

    def menus(self):
        """
        Displays the available menu options.
        """

        print(
            """
        Menu
        1. Tambah item
        2. Ubah nama item
        3. Ubah jumlah item
        4. Ubah harga item
        5. Hapus item
        6. Reset transaksi
        7. Cek order
        8. Checkout
        """
        )
        menu = input("Pilih menu (tuliskan nomor): ")

        try:
            self.user_option = int(menu)
        except ValueError:
            print("Error: Pilih menu menggunakan nomor!")

    def transaction(self):
        """
        Sets the transaction ID.
        """
        self.transaction_id = input("Buat ID Transaksi Anda: ").upper()
        print("ID Transaksi Anda: " + self.transaction_id)

    def add_item(self, item_name, item_quantity, item_price):
        """
        Adds an item to the order.

        Args:
            item_name (str): The name of the item.
            item_quantity (int): The quantity of the item.
            item_price (int): The price of the item.
        """

        print("=" * 40)

        # Error defense if Customer doesn't input item_quantity and
        # item_price in number format
        try:
            # Store item into 'item' variable
            item = {"item_name": item_name.capitalize(),
                    "item_quantity": int(item_quantity),
                    "item_price": int(item_price),
                    "total_price": int(int(item_quantity) * int(item_price))}

            # Add 'item' into 'items' list
            self.items.append(item)

            print("Info: Item berhasil ditambahkan!")
            print("=" * 40)

            # Reset user option
            self.user_option = 0

        # Throw error message if item_quantity and
        # item_price not in number format
        except ValueError:
            print("Error: Jumlah barang atau Harga barang yang anda masukkan"
                  " tidak valid!\n> Hanya boleh memasukkan angka!")

    def update_item_name(self, old_item_name, new_item_name):
        """
        Updates the name of an item in the order.

        Args:
            old_item_name (str): The current name of the item.
            new_item_name (str): The new name for the item.
        """

        print("=" * 40)
        print("Ubah nama item")

        # Find index number of item
        item_index = get_index(self.items, "item_name", old_item_name)

        if item_index == -1:
            print("Error: Gagal mengubah nama item. Item tidak ditemukan!")
        else:
            # Modify item name
            self.items[item_index]["item_name"] = new_item_name.capitalize()

            print("Info: Nama item berhasil diubah!")
            print("=" * 40)

            # Reset user option
            self.user_option = 0

    def update_item_qty(self, item_name, new_item_qty):
        """
        Updates the quantity of an item in the order.

        Args:
            item_name (str): The name of the item.
            new_item_qty (int): The new quantity for the item.
        """

        print("=" * 40)
        print("Ubah jumlah item")

        # Find index number of item
        item_index = get_index(self.items, "item_name", item_name)

        try:
            if item_index == -1:
                print("Error: Gagal mengubah jumlah item."
                      "Item tidak ditemukan!")
            else:
                # Modify item quantity
                self.items[item_index]["item_quantity"] = int(new_item_qty)

                # Modify item total_price because item quantity has changed
                item_quantity = self.items[item_index]["item_quantity"]
                item_price = self.items[item_index]["item_price"]

                self.items[item_index]["total_price"] = int(
                    int(item_quantity) * int(item_price))

                print("Info: Jumlah item berhasil diubah!")
                print("=" * 40)

                # Reset user option
                self.user_option = 0
        except ValueError:
            print("Error: Jumlah item harus dalam format angka!")

    def update_item_price(self, item_name, new_item_price):
        """
        Updates the price of an item in the order.

        Args:
            item_name (str): The name of the item.
            new_item_price (int): The new price for the item.
        """

        print("=" * 40)
        print("Ubah harga item")

        # Find index number of item
        item_index = get_index(self.items, "item_name", item_name)

        try:
            if item_index == -1:
                print("Error: Gagal mengubah harga item!"
                      "Item tidak ditemukan!")
            else:
                # Modify item price
                self.items[item_index]["item_price"] = int(new_item_price)

                # Modify item total_price because item price has changed
                item_quantity = self.items[item_index]["item_quantity"]
                item_price = self.items[item_index]["item_price"]

                self.items[item_index]["total_price"] = int(
                    int(item_quantity) * int(item_price))

                print("Info: Harga item berhasil diubah!")
                print("=" * 40)

                # Reset user option
                self.user_option = 0
        except ValueError:
            print("Error: Harga item harus dalam format angka!")

    def delete_item(self, item_name):
        """
        Deletes an item from the order.

        Args:
            item_name (str): The name of the item to delete.
        """

        print("=" * 40)
        print("Hapus item")

        # Find index number of item
        item_index = get_index(self.items, "item_name", item_name)

        if item_index == -1:
            print("Error: Gagal menghapus item! Item tidak ditemukan!")
        else:
            # Remove item
            self.items.pop(item_index)

            print("Info: Item berhasil dihapus!")
            print("=" * 40)

            # Reset user option
            self.user_option = 0

    def reset_transaction(self):
        """
        Resets the transaction by clearing the items in the order.
        """

        print("=" * 40)
        print("Reset transaksi")

        self.items.clear()

        print("Info: Reset transaksi berhasil!")

        # Reset user option
        self.user_option = 0

    def check_order(self):
        """
        Displays the items in the current order.
        """

        print("=" * 40)
        print("Check Order")

        if len(self.items) > 0:

            # Create table
            items_table = PrettyTable(["No.", "Nama Item", "Jumlah Item",
                                       "Harga Item", "Total Harga"])

            # Add data into row
            for i in range(len(self.items)):
                items_table.add_row([
                    i + 1,
                    self.items[i]["item_name"],
                    self.items[i]["item_quantity"],
                    currency_conversion(self.items[i]["item_price"]),
                    currency_conversion(self.items[i]["total_price"])
                ])

            # Show order details
            print(items_table)

            # Show message
            print("Info: Pemesanan sudah benar!")
        else:
            print("Info: Item kosong!")

        # Reset user option
        self.user_option = 0

    def check_out(self):
        """
        Processes the checkout by calculating the total price, applying
        discounts, and inserting the transaction into the database.

        Returns:
            bool: False if item is empty.
        """

        print("=" * 40)
        print("Checkout!")

        if len(self.items) == 0:
            print("Info: Item kosong. Tidak bisa melakukan Check Out!")
            return False

        order_table = PrettyTable(["No.", "Nama Item",
                                   "Jumlah Item",
                                   "Harga Item",
                                   "Total Harga",
                                   "Diskon",
                                   "Harga setelah diskon"])

        self.order = [item for item in self.items]

        # Check discount
        for i in range(len(self.order)):
            discount = self.check_discount(self.order[i]["total_price"])

            if discount is False:
                self.order[i]["discount"] = None
                self.order[i]["price_after_discount"] = None
                self.grand_total += self.order[i]["total_price"]
            else:
                self.order[i]["discount"] = discount["discount"]
                self.order[i]["price_after_discount"] = discount["total"]
                self.grand_total += self.order[i]["price_after_discount"]

            order_table.add_row([
                i + 1,
                self.order[i]["item_name"],
                self.order[i]["item_quantity"],
                currency_conversion(self.order[i]["item_price"]),
                currency_conversion(self.order[i]["total_price"]),
                currency_conversion(self.order[i]["discount"]),
                currency_conversion(self.order[i]["price_after_discount"])
            ])

        # Show order details
        print(order_table)
        print("Total Bayar: {}".format(currency_conversion(self.grand_total)))

        print("Terima Kasih sudah berbelanja :)")

        # Insert transaction into sqlite
        self.insert_to_table()
