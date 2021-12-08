import os
import sys
import datetime
import uuid #UUID generator
import pandas as pd # Impor pandas untuk tampilan table
from termcolor import colored, cprint # Impor termcolor modules
from dotenv import load_dotenv as LoadDotEnv # Impor env modules
LoadDotEnv() # Load env data
from tabulate import tabulate # Tabulate
from config.conn import conn, sqlite3 # Impor koneksi database file (config/conn.py)

# Deklarasi variabel dari env
APP_BRAND_NAME = os.getenv('APP_BRAND_NAME')
APP_BRAND_ADDRESS = os.getenv('APP_BRAND_ADDRESS')
APP_BRAND_EMAIL = os.getenv('APP_BRAND_EMAIL')
APP_BRAND_PHONE_NUMBER = os.getenv('APP_BRAND_PHONE_NUMBER')

# Fungsi produk model
def ProdukGetAll():
	data = pd.read_sql_query("SELECT kode as KODE, nama as NAMA, harga as HARGAperKG from produk", conn)
	data.reset_index(drop=True)
	print(tabulate(data, headers='keys', tablefmt='psql'))
def ProdukShow(kode):
	data = conn.execute("SELECT kode as KODE, nama as NAMA, harga as HARGA from produk WHERE kode='"+str(kode)+"'")
	return data.fetchall()
def ProdukInsert(data):
	conn.execute("INSERT INTO produk (nama, harga) VALUES ('"+str(data["nama"])+"', "+str(data["harga"])+")")
	conn.commit()
def ProdukUpdate(data):
	try:
		conn.execute("UPDATE produk SET nama='"+str(data["nama"])+"', harga="+str(data["harga"])+" WHERE kode="+str(data["kode"]))
		conn.commit()
	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
def ProdukDelete(kode):
	try:
		conn.execute("DELETE FROM produk WHERE kode="+str(kode)+"")
		conn.commit()
		return True
	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)

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
	conn.execute("UPDATE transaksi SET total='"+str(data["total"])+"', bayar='"+str(data["bayar"])+"', kembali='"+str(data["kembali"])+"' WHERE kode='"+str(data["kode"])+"'")
	conn.commit()

# Fungsi transaksi produk model
def TransaksiProdukGetAll(transaksi_kode):
	data = pd.read_sql_query("SELECT produk.nama, transaksi_produk.jumlah, transaksi_produk.total FROM transaksi_produk INNER JOIN produk ON produk.kode=transaksi_produk.produk_kode WHERE transaksi_produk.transaksi_kode='"+str(transaksi_kode)+"'", conn)
	data.reset_index(drop=True)
	print(tabulate(data, headers='keys', tablefmt='psql'))
	data2 = conn.execute("SELECT produk.nama, transaksi_produk.jumlah, transaksi_produk.total FROM transaksi_produk INNER JOIN produk ON produk.kode=transaksi_produk.produk_kode WHERE transaksi_produk.transaksi_kode='"+str(transaksi_kode)+"'")
	return data2.fetchall()
def TransaksiProdukInsert(data):
	conn.execute("INSERT INTO transaksi_produk (transaksi_kode, produk_kode, jumlah, total) VALUES ('"+str(data["transaksi_kode"])+"', '"+str(data["produk_kode"])+"', '"+str(data["jumlah"])+"', '"+str(data["total"])+"')")
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
				os.system('cls')
				ProdukGetAll()
				ask = input("Input (b) untuk kembali ke menu data produk, atau (q) untuk keluar: \n")
				if ask == "b" or ask == "B":
					os.system('cls')
					MenuManagementProduk()
				elif ask == "q" or ask == "Q":
					break
				else:
					os.system('cls')
					print(colored("Input data sesuai yang di menu", "red"))
					MenuManagementProduk()
			elif navigation == 2:
				os.system('cls')
				data = {}
				data["nama"] = input("Masukkan nama produk: \n")
				data["harga"] = input("Masukkan harga produk: \n")
				if data["nama"] != "" and data["harga"] != "":
					if not data["nama"].isnumeric():
						if data["harga"].isnumeric():
							ProdukInsert(data)
							os.system('cls')
							print(colored("Berhasil menambah data produk", "green"))
							MenuManagementProduk()
						else:
							os.system('cls')
							print(colored("Harga yang dimasukkan harus berupa angka", "red"))
							MenuManagementProduk()
					else:
						os.system('cls')
						print(colored("Data tidak sesuai", "red"))
						MenuManagementProduk()
				else:
					os.system('cls')
					print(colored("Input data sesuai yang di menu", "red"))
					MenuManagementProduk()
			elif navigation == 3:
				os.system('cls')
				ProdukGetAll()
				data = {}
				data["kode"] = input("Masukkan kode produk yang ingin di edit: \n")
				data["nama"] = input("Masukkan nama produk: \n")
				data["harga"] = input("Masukkan harga produk: \n")
				if data["kode"] != "" and data["nama"] != "" and data["harga"] != "":
					if not data["nama"].isnumeric():
						if data["harga"].isnumeric():
							if (ProdukUpdate(data)):
								os.system('cls')
								print(colored("Berhasil memperbarui data produk", "green"))
								MenuManagementProduk()
							else:
								os.system('cls')
								print(colored("Data tidak sesuai", "red"))
								MenuManagementProduk()
						else:
							os.system('cls')
							print(colored("Harga yang dimasukkan harus berupa angka", "red"))
							MenuManagementProduk()
					else:
						os.system('cls')
						print(colored("Data tidak sesuai", "red"))
						MenuManagementProduk()
				else:
					os.system('cls')
					print(colored("Input data sesuai yang di menu", "red"))
					MenuManagementProduk()
			elif navigation == 4:
				os.system('cls')
				ProdukGetAll()
				kode = input("Masukkan kode produk yang ingin di hapus: \n")
				if kode != "":
					if ProdukDelete(kode):
						os.system('cls')
						print(colored("Berhasil menghapus data produk", "green"))
						MenuManagementProduk()
					else:
						os.system('cls')
						print(colored("Data tidak sesuai", "red"))
						MenuManagementProduk()
				else:
					os.system('cls')
					print(colored("Input data sesuai yang di menu", "red"))
					MenuManagementProduk()
			elif navigation == 5:
				os.system('cls')
				MenuMain()
			else:
				os.system('cls')
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
					os.system('cls')
					print(colored("------------------------------------------------------------------", "yellow"))
					print(colored("Kode Transaksi: " + transaksi, "yellow"))
					print(colored("Nama Kasir: " + nama_kasir, "yellow"))
					print(colored("------------------------------------------------------------------", "yellow"))
					show_produk = ProdukShow(produk)
					if show_produk and show_produk[0]:
						data_produk_transaksi = {}
						data_produk_transaksi["transaksi_kode"] = transaksi
						data_produk_transaksi["produk_kode"] = show_produk[0][0]
						data_produk_transaksi["jumlah"] = produk_jumlah
						data_produk_transaksi["total"] = int(produk_jumlah * show_produk[0][2])
						TransaksiProdukInsert(data_produk_transaksi)
						keranjangs = TransaksiProdukGetAll(transaksi)
						ask = input("Input (y) untuk konfirmasi produk, atau (r) untuk menambah produk lainnya: ")
						if (ask == "y"):
							total_harga = 0
							for keranjang in keranjangs:
								total_harga += keranjang[2]
							data_transaksi = {}
							data_transaksi["kode"] = transaksi
							data_transaksi["total"] = total_harga
							data_transaksi["bayar"] = int(input("Pelanggan membayar uang sebanyak: "))
							if (data_transaksi["bayar"] < total_harga):
								os.system('cls')
								print(colored("Maaf, Uang yang dibayar kurang!", "red"))
								TransaksiProduk()
							else:
								data_transaksi["kembali"] = int(int(data_transaksi["bayar"]) - total_harga)
								now = datetime.datetime.now()
								TransaksiUpdatePembayaran(data_transaksi)
								print(colored(f"""
================================================
              Buah Segar ID Bill
{now.strftime ("%Y-%m-%d %H:%M:%S")}
================================================
{transaksi}
Nama Kasir           :  {nama_kasir} 
================================================""","green"))
							for keranjang in keranjangs:
								print(colored(f"""
jenis buah           : {str(keranjang[0])}
jumlah buah          : {str(keranjang[1])} KG
harga total          : RP  {str(keranjang[2])}""","green"))
							print(colored(f"""================================================
Total                : RP  {str(total_harga)}
Bayar                : RP  {str(data_transaksi["bayar"])}
kembali              : RP  {str(data_transaksi["kembali"])}
Barang yang sudah dibeli tidak dapat ditukar !!! ""","green"))
							MenuMain()
						else:
							continue
					else:
						os.system('cls')
						print(colored("Pilih kode produk yang ada di atas!", "red"))
			except ValueError as err:
				os.system('cls')
				print(colored(err, "red"))
				continue
	else:
		os.system('cls')
		print(colored("Kesalahan! anda akan dialihkan ke halaman utama", "red"))
		MenuMain()

def HistoriTransaksi():
	TransaksiGetAll()
	# Perulangan while, supaya pertanyaan berulang jika user salah input pilihan
	while True:
		try:
			ask = input("Input (y) untuk kembali ke menu awal: ")
			if ask == "y":
				os.system('cls')
				MenuMain()
			else:
				continue
		except ValueError as err:
			print(colored("Masukkan pilihan menu dengan benar!", "red"))


# Fungsi tampilan menu utama
def MenuMain():
	print("==============================================")
	print("\t\t🥝 " + APP_BRAND_NAME)
	print("==============================================")
	print("1. Manajemen data produk")
	print("2. Buat transaksi pelanggan")
	print("3. Lihat semua histori transaksi")
	print("==============================================")

	# Perulangan while, supaya pertanyaan berulang jika user salah input pilihan
	while True:
		try:
			navigation = int(input("Pilih menu di atas untuk melanjutkan aksi: ")) # Input untuk navigasi menu
			if navigation == 1:
				MenuManagementProduk()
				break
			elif navigation == 2:
				TransaksiProduk()
				break
			elif navigation == 3:
				HistoriTransaksi()
				break
			else:
				print(colored("Masukkan pilihan menu dengan benar!", "red"))
				continue
		except ValueError as err:
			print(colored("Masukkan pilihan menu dengan benar!", "red"))

# Load main menu

os.system('cls')
MenuMain()