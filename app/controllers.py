import os
import sys
import datetime
from termcolor import colored, cprint # Impor termcolor modules
import app.models as models # Impor models file
import app.home as home # Impor home file

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
			navigation = int(input("Pilih menu di atas untuk melanjutkan aksi: ")) # Input untuk navigasi menu
			if navigation == 1:
				os.system('cls')
				models.ProdukGetAll()
				ask = input("Input (Y) untuk kembali ke menu data produk, atau (N) untuk keluar: ")
				if ask == "Y" or ask == "y":
					os.system('cls')
					MenuManagementProduk()
				elif ask == "n" or ask == "N":
					break
				else:
					os.system('cls')
					print(colored("Input data sesuai yang di menu", "red"))
					MenuManagementProduk()
			elif navigation == 2:
				os.system('cls')
				data = {}
				data["nama"] = input("Masukkan nama produk: ")
				data["harga"] = input("Masukkan harga produk: ")
				if data["nama"] != "" and data["harga"] != "":
					if not data["nama"].isnumeric():
						if data["harga"].isnumeric():
							models.ProdukInsert(data)
							os.system('cls')
							print(colored("Berhasil menambah data produk", "green"))
							MenuManagementProduk()
						else:
							os.system('cls')
							print(colored("DATA TIDAK DIKENAL", "red"))
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
				models.ProdukGetAll()
				data = {}
				data["kode"] = input("Masukkan kode produk yang ingin di edit: ")
				data["nama"] = input("Masukkan nama produk: ")
				data["harga"] = input("Masukkan harga produk: ")
				if data["kode"] != "" and data["nama"] != "" and data["harga"] != "":
					if not data["nama"].isnumeric():
						if data["harga"].isnumeric():
							if models.ProdukUpdate(data):
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
				models.ProdukGetAll()
				kode = input("Masukkan kode produk yang ingin di hapus: ")
				if kode != "":
					if models.ProdukDelete(kode):
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
				home.MenuMain()
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
	if (confirm_create_transaksi == "y" or confirm_create_transaksi == "Y"):
		nama_kasir = input("Masukkan nama Kasir: ")
		data_transaksi = {}
		data_transaksi["nama_kasir"] = nama_kasir
		data_transaksi["total"] = 0
		data_transaksi["bayar"] = 0
		data_transaksi["kembali"] = 0
		transaksi = models.TransaksiInsert(data_transaksi)
		print(colored("Transaksi berhasil di buat dengan kode: " + transaksi, "green"))
		# Perulangan while, untuk multiple produk dalam satu transaksi
		while True:
			try:
					models.ProdukGetAll() # Tampilkan data produk
					produk = int(input("Masukkan kode produk untuk ditambahkan ke daftar transaksi: ")) # Input untuk kode produk
					produk_jumlah = int(input("Masukkan jumlah pembelian pada produk: ")) # Input jumlah
					os.system('cls')
					print(colored("------------------------------------------------------------------", "green"))
					print(colored("Kode Transaksi: " + transaksi, "green"))
					print(colored("Nama Kasir: " + nama_kasir, "green"))
					print(colored("------------------------------------------------------------------", "green"))
					show_produk = models.ProdukShow(produk)
					if show_produk and show_produk[0]:
						data_produk_transaksi = {}
						data_produk_transaksi["transaksi_kode"] = transaksi
						data_produk_transaksi["produk_kode"] = show_produk[0][0]
						data_produk_transaksi["jumlah"] = produk_jumlah
						data_produk_transaksi["total"] = int(produk_jumlah * show_produk[0][2])
						models.TransaksiProdukInsert(data_produk_transaksi)
						keranjangs = models.TransaksiProdukGetAll(transaksi)
						ask = input("Input (y) untuk konfirmasi produk, atau (r) untuk menambah produk lainnya: ")
						if (ask == "y" or ask == "Y"):
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
								models.TransaksiUpdatePembayaran(data_transaksi)
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
							home.MenuMain()
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
		home.MenuMain()

def HistoriTransaksi():
	models.TransaksiGetAll()
	# Perulangan while, supaya pertanyaan berulang jika user salah input pilihan
	while True:
		try:
			ask = input("Input (y) untuk kembali ke menu awal: ")
			if ask == "y":
				os.system('cls')
				home.MenuMain()
			else:
				continue
		except ValueError as err:
			print(colored("Masukkan pilihan menu dengan benar!", "red"))
