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
				data = pd.read_sql_query("SELECT kode as KODE, nama as NAMA, harga as HARGA from product", conn)
				data.reset_index(drop=True)
				print(tabulate(data, headers='keys', tablefmt='psql'))
				ask = input("Input (y) untuk kembali, input apapun untuk keluar: \n")
				if ask == "y":
					MenuManagementProduct()
				else:
					break
			elif navigation == 2:
				nama = input("Masukkan nama produk: \n")
				harga = int(input("Masukkan harga produk: \n"))
				conn.execute("INSERT INTO product (nama, harga) VALUES ('"+str(nama)+"', "+str(harga)+")")
				conn.commit()
				print("Berhasil menambah data produk")
				ask = input("Input (y) untuk kembali, input apapun untuk keluar: \n")
				if ask == "y":
					MenuManagementProduct()
				else:
					break
			elif navigation == 3:
				print("LIHAT PRODUK")
				break
			elif navigation == 4:
				print("LIHAT PRODUK")
				break
			elif navigation == 5:
				MenuMain()
			else:
				print("Masukkan pilihan menu dengan benar!")
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
				print("Masukkan pilihan menu dengan benar!")
				continue
		except ValueError as err:
			print("Masukkan pilihan menu dengan benar!")

# Load main menu
MenuMain()