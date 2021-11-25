import os
import sys
import uuid #UUID generator
import pandas as pd # Impor pandas untuk tampilan table
from termcolor import colored, cprint # Impor termcolor modules
from dotenv import load_dotenv as LoadDotEnv # Impor env modules
LoadDotEnv() # Load env data
from tabulate import tabulate # Tabulate
from config.conn import conn # Impor koneksi database file (config/conn.py)

# Deklarasi variabel dari env
APP_BRAND_NAME = os.getenv('APP_BRAND_NAME')
APP_BRAND_ADDRESS = os.getenv('APP_BRAND_ADDRESS')
APP_BRAND_EMAIL = os.getenv('APP_BRAND_EMAIL')
APP_BRAND_PHONE_NUMBER = os.getenv('APP_BRAND_PHONE_NUMBER')

# Fungsi produk model
def ProdukGetAll():
	data = pd.read_sql_query("SELECT kode as KODE, nama as NAMA, harga as HARGA from produk", conn)
	data.reset_index(drop=True)
	print(tabulate(data, headers='keys', tablefmt='psql'))
def ProdukShow(kode):
	data = conn.execute("SELECT kode as KODE, nama as NAMA, harga as HARGA from produk WHERE kode='"+str(kode)+"'")
	return data.fetchall()
def ProdukInsert(data):
	conn.execute("INSERT INTO produk (nama, harga) VALUES ('"+str(data["nama"])+"', "+str(data["harga"])+")")
	conn.commit()
def ProdukUpdate(data):
	conn.execute("UPDATE produk SET nama='"+str(data["nama"])+"', harga="+str(data["harga"])+" WHERE kode="+str(data["kode"]))
	conn.commit()
def ProdukDelete(kode):
	conn.execute("DELETE FROM produk WHERE kode="+str(kode)+"")
	conn.commit()

# Fungsi transaksi model
def TransaksiGetAll():
	data = pd.read_sql_query("SELECT kode as KODE, nama_kasir as NAMA_KASIR, total as TOTAL, bayar as BAYAR, kembali as KEMBALI, tanggal as TANGGAL from transaksi", conn)
	data.reset_index(drop=True)
	print(tabulate(data, headers='keys', tablefmt='psql'))
def TransaksiInsert(data):
	generate_unik_kode = uuid.uuid1()
	conn.execute("INSERT INTO transaksi (kode, nama_kasir, total, bayar, kembali) VALUES ('"+str(generate_unik_kode)+"', '"+str(data["nama_kasir"])+"', '"+str(data["total"])+"', '"+str(data["bayar"])+"', '"+str(data["kembali"])+"')")
	conn.commit()
	return str(generate_unik_kode)
def TransaksiUpdatePembayaran(data):
	conn.execute("UPDATE produk SET total='"+str(data["total"])+"', bayar='"+str(data["bayar"])+"', kembali='"+str(data["kembali"])+"' WHERE kode="+str(data["kode"]))
	conn.commit()

# Fungsi transaksi produk model
def TransaksiProdukInsert(data):
	conn.execute("INSERT INTO transaksi (transaksi_id, produk_id, jumlah, total) VALUES ('"+str(data["transaksi_id"])+"', '"+str(data["produk_id"])+"', '"+str(data["jumlah"])+"', '"+str(data["total"])+"')")
	conn.commit()

# Fungsi tampilan menu manajemen produk
def MenuManagementProduk():
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
				ProdukGetAll()
				ask = input("Input (y) untuk kembali, input apapun untuk keluar: \n")
				if ask == "y":
					MenuManagementProduk()
				else:
					break
			elif navigation == 2:
				data = {}
				data["nama"] = input("Masukkan nama produk: \n")
				data["harga"] = int(input("Masukkan harga produk: \n"))
				ProdukInsert(data)
				print(colored("Berhasil menambah data produk", "green"))
				MenuManagementProduk()
			elif navigation == 3:
				ProdukGetAll()
				data = {}
				data["kode"] = input("Masukkan kode produk yang ingin di edit: \n")
				data["nama"] = input("Masukkan nama produk: \n")
				data["harga"] = int(input("Masukkan harga produk: \n"))
				ProdukUpdate(data)
				print(colored("Berhasil memperbarui data produk", "green"))
				MenuManagementProduk()
			elif navigation == 4:
				ProdukGetAll()
				kode = input("Masukkan kode produk yang ingin di hapus: \n")
				ProdukDelete(kode)
				print(colored("Berhasil menghapus data produk", "green"))
				MenuManagementProduk()
			elif navigation == 5:
				MenuMain()
			else:
				print(colored("Masukkan pilihan menu dengan benar!", "red"))
				continue
		except ValueError as err:
			print(err)
			continue

# Fungsi tampilan transaksi produk
def TransaksiProduk():
	confirm_create_transaksi = input("Input (y) untuk membuat transaksi baru: ") # Input untuk generate data transaksi
	if (confirm_create_transaksi == "y"):
		nama_kasir = input("Masukkan nama Kasir: ")
		data_transaksi = {}
		data_transaksi["nama_kasir"] = nama_kasir
		data_transaksi["total"] = 0
		data_transaksi["bayar"] = 0
		data_transaksi["kembali"] = 0
		transaksi = TransaksiInsert(data_transaksi)
		print(colored("Transaksi berhasil di buat dengan kode: " + transaksi, "green"))
		# Perulangan while, untuk multiple produk dalam satu transaksi
		while True:
			try:
					ProdukGetAll() # Tampilkan data produk
					produk = int(input("Masukkan kode produk untuk ditambahkan ke daftar transaksi: ")) # Input untuk kode produk
					produk_jumlah = int(input("Masukkan jumlah pembelian pada produk: ")) # Input jumlah
					print(colored("------------------------------------------------------------------", "green"))
					print(colored("Kode Transaksi: " + transaksi, "green"))
					print(colored("Nama Kasir: " + nama_kasir, "green"))
					print(colored("------------------------------------------------------------------", "green"))
					show_produk = ProdukShow(produk)
					print(show_produk)
					if show_produk:
						data_produk_transaksi = {}
						data_produk_transaksi["transaksi_id"] = transaksi
						data_produk_transaksi["produk_id"] = produk.kode
						data_produk_transaksi["jumlah"] = produk_jumlah
						data_produk_transaksi["total"] = (produk_jumlah * produk.harga)
						print(data_produk_transaksi)
						# TransaksiProdukInsert(data_produk_transaksi)
						ask = input("Input (y) untuk konfirmasi produk, atau (r) untuk menambah produk lainnya: ")
						if (ask == "y"):
							print("selesai bro")
						else:
							continue
					else:
						print(colored("Pilih kode produk yang ada di atas!", "red"))
			except ValueError as err:
				print(colored(err, "red"))
				continue
	else:
		print(colored("Kesalahan! anda akan dialihkan ke halaman utama", "red"))
		MenuMain()

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
				MenuManagementProduk()
				break
			elif navigation == 2:
				TransaksiProduk()
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