import os
import sys
from termcolor import colored, cprint # Impor termcolor modules
from dotenv import load_dotenv as LoadDotEnv # Impor env modules
LoadDotEnv() # Load env data
from config.conn import conn # Impor koneksi database file (config/conn.py)
import pandas as pd # Impor pandas untuk tampilan table
from tabulate import tabulate

# Deklarasi variabel dari env
APP_BRAND_NAME = os.getenv('APP_BRAND_NAME')
APP_BRAND_ADDRESS = os.getenv('APP_BRAND_ADDRESS')
APP_BRAND_EMAIL = os.getenv('APP_BRAND_EMAIL')
APP_BRAND_PHONE_NUMBER = os.getenv('APP_BRAND_PHONE_NUMBER')

# Fungsi produk controller
def ProductGetAll():
	data = pd.read_sql_query("SELECT kode as KODE, nama as NAMA, harga as HARGA from product", conn)
	data.reset_index(drop=True)
	print(tabulate(data, headers='keys', tablefmt='psql'))
def ProductInsert(data):
	conn.execute("INSERT INTO product (nama, harga) VALUES ('"+str(data["nama"])+"', "+str(data["harga"])+")")
	conn.commit()
def ProductUpdate(data):
	conn.execute("UPDATE product SET nama='"+str(data["nama"])+"', harga="+str(data["harga"])+" WHERE kode="+str(data["kode"]))
	conn.commit()
def ProductDelete(kode):
	conn.execute("DELETE FROM product WHERE kode="+str(kode)+"")
	conn.commit()

# Fungsi tampilan menu manajemen produk
def MenuManagementProduct():
	print("-------------------------------------")
	print("\t Manajemen Data Produk")
	print("-------------------------------------")
	print("1. Lihat data produk")
	print("2. Tambah produk baru")
	print("3. Edit produk")
	print("4. Hapus produk")
	print("5. Kembali ke Menu Awal")
	print("-------------------------------------")

	# Perulangan while, supaya pertanyaan berulang jika user salah input pilihan
	while True:
		try:
			navigation = int(input("Pilih menu di atas untuk melanjutkan aksi: \n")) # Input untuk navigasi menu
			if navigation == 1:
				ProductGetAll()
				ask = input("Input (y) untuk kembali, input apapun untuk keluar: \n")
				if ask == "y":
					MenuManagementProduct()
				else:
					break
			elif navigation == 2:
				data = {}
				data["nama"] = input("Masukkan nama produk: \n")
				data["harga"] = int(input("Masukkan harga produk: \n"))
				ProductInsert(data)
				print(colored("Berhasil menambah data produk", "green"))
				MenuManagementProduct()
			elif navigation == 3:
				ProductGetAll()
				data = {}
				data["kode"] = input("Masukkan kode produk yang ingin di edit: \n")
				data["nama"] = input("Masukkan nama produk: \n")
				data["harga"] = int(input("Masukkan harga produk: \n"))
				ProductUpdate(data)
				print(colored("Berhasil memperbarui data produk", "green"))
				MenuManagementProduct()
			elif navigation == 4:
				ProductGetAll()
				kode = input("Masukkan kode produk yang ingin di hapus: \n")
				ProductDelete(kode)
				print(colored("Berhasil menghapus data produk", "green"))
				MenuManagementProduct()
			elif navigation == 5:
				MenuMain()
			else:
				print(colored("Masukkan pilihan menu dengan benar!", "red"))
				continue
		except ValueError as err:
			print(err)
			continue

# Fungsi tampilan menu utama
def MenuMain():
	print("==============================================")
	print("\t\t🍓 " + APP_BRAND_NAME)
	print("==============================================")
	print("1. Manajemen data produk")
	print("2. Buat transaksi pelanggan")
	print("3. Lihat semua histori transaksi")
	print("==============================================")

	# Perulangan while, supaya pertanyaan berulang jika user salah input pilihan
	while True:
		try:
			navigation = int(input("Pilih menu di atas untuk melanjutkan aksi: \n")) # Input untuk navigasi menu
			if navigation == 1:
				MenuManagementProduct()
				break
			elif navigation == 2:
				print("BUAT TRANSAKSI")
				break
			elif navigation == 3:
				print("TAMPILKAN HISTORI TRANSAKSI")
				break
			else:
				print(colored("Masukkan pilihan menu dengan benar!", "red"))
				continue
		except ValueError as err:
			print(colored("Masukkan pilihan menu dengan benar!", "red"))

# Load main menu
MenuMain()