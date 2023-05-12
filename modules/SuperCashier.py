# A library change Dictionary to JSON format
import json


class SuperCashier:
    def __init__(self):
        self.transaction_id = ""
        self.items = []
        self.order = []
        self.user_option = 0

    def get_index(self, key, value):
        for i in range(len(self.items)):
            if self.items[i][key].lower() == value.lower():
                return i
        return -1

    def check_discount(self, total_price):
        if total_price > 200_000 and total_price <= 300_000:
            discount = total_price * (5/100)
            return total_price - discount
        elif total_price > 300_000 and total_price <= 500_000:
            discount = total_price * (6/100)
            return total_price - discount
        elif total_price > 500_000:
            discount = total_price * (7/100)
            return total_price - discount
        else:
            return total_price

    def menus(self):
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
            print("> Pilih menu menggunakan nomor!")

    def transaction(self):
        self.transaction_id = input("Buat ID Transaksi Anda: ")
        print("ID Transaksi Anda: " + self.transaction_id)

    def add_item(self):
        print("=" * 40)
        item_name = input("Masukkan nama item: ")
        item_quantity = input("Masukkan jumlah item: ")
        item_price = input("Masukkan harga item: ")

        # Error defense if Customer doesn't input item_quantity and
        # item_price in number format

        try:
            # Store item into 'item' variable
            item = {"item_name": item_name,
                    "item_quantity": int(item_quantity),
                    "item_price": int(item_price),
                    "total_price": int(int(item_quantity) * int(item_price))}

            # Add 'item' into 'items' list
            self.items.append(item)

            print("> Item berhasil ditambahkan!")
            print("=" * 40)

            # Reset user option
            self.user_option = 0

        # Throw error message if item_quantity and
            # item_price not in number format
        except ValueError:
            print("> Jumlah barang atau Harga barang yang anda masukkan tidak"
                  "valid!\n> Hanya boleh memasukkan angka!")

    def update_item_name(self):
        print("=" * 40)
        print("Ubah nama item")

        old_item_name = input("Masukkan nama item yang ingin diubah: ")
        new_item_name = input("Masukkan nama item yang baru: ")

        # Find index number of item
        item_index = self.get_index("item_name", old_item_name)

        if item_index == -1:
            print("> Gagal mengubah nama item!")
            print("> Item tidak ditemukan!")
        else:
            # Modify item name
            self.items[item_index]["item_name"] = new_item_name

            print("> Nama item berhasil diubah!")
            print("=" * 40)

            # Reset user option
            self.user_option = 0

    def update_item_qty(self):
        print("=" * 40)
        print("Ubah jumlah item")

        item_name = input("Masukkan nama item yang ingin diubah jumlahnya: ")
        new_item_qty = input("Masukkan jumlah item yang baru: ")

        # Find index number of item
        item_index = self.get_index("item_name", item_name)

        try:
            if item_index == -1:
                print("> Gagal mengubah jumlah item!")
                print("> Item tidak ditemukan!")
            else:
                # Modify item quantity
                self.items[item_index]["item_quantity"] = int(new_item_qty)

                print("> Jumlah item berhasil diubah!")
                print("=" * 40)

                # Reset user option
                self.user_option = 0
        except ValueError:
            print("> Jumlah item harus dalam format angka!")

    def update_item_price(self):
        print("=" * 40)
        print("Ubah harga item")

        item_name = input("Masukkan nama item yang ingin diubah harganya: ")
        new_item_price = input("Masukkan harga item yang baru: ")

        # Find index number of item
        item_index = self.get_index("item_name", item_name)

        try:
            if item_index == -1:
                print("> Gagal mengubah harga item!")
                print("> Item tidak ditemukan!")
            else:
                # Modify item price
                self.items[item_index]["item_price"] = int(new_item_price)

                print("> Harga item berhasil diubah!")
                print("=" * 40)

                # Reset user option
                self.user_option = 0
        except ValueError:
            print("> Harga item harus dalam format angka!")

    def delete_item(self):
        print("=" * 40)
        print("Hapus item")

        item_name = input("Masukkan nama item yang ingin dihapus: ")

        # Find index number of item
        item_index = self.get_index("item_name", item_name)

        if item_index == -1:
            print("> Gagal menghapus item!")
            print("> Item tidak ditemukan!")
        else:
            # Remove item
            self.items.pop(item_index)

            print("> Item berhasil dihapus!")
            print("=" * 40)

            # Reset user option
            self.user_option = 0

    def reset_transaction(self):
        print("=" * 40)
        print("Reset transaksi")

        self.items.clear()

        print("> Reset transaksi berhasil!")

        # Reset user option
        self.user_option = 0

    def check_order(self):
        print("=" * 40)
        print("Check Order")

        self.order = [item for item in self.items]

        # Check discount
        for i in range(len(self.order)):
            self.order[i]["price_after_discount"] = self.check_discount(
                self.order[i]["total_price"])

        # Show order details
        print(json.dumps(self.order, indent=4))

        # Reset user option
        self.user_option = 0

    def check_out(self):
        print("Checkout!")
        print("Terima Kasih sudah berbelanja :)")
