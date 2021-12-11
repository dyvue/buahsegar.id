import os
from termcolor import colored, cprint # Impor termcolor modules
from dotenv import load_dotenv as LoadDotEnv # Impor env modules
LoadDotEnv() # Load env data
import app.controllers as controllers # Impor controllers file

# Deklarasi variabel dari env
APP_BRAND_NAME = os.getenv('APP_BRAND_NAME')
APP_BRAND_ADDRESS = os.getenv('APP_BRAND_ADDRESS')
APP_BRAND_EMAIL = os.getenv('APP_BRAND_EMAIL')
APP_BRAND_PHONE_NUMBER = os.getenv('APP_BRAND_PHONE_NUMBER')

# Fungsi tampilan menu utama
def MenuMain():
	print("==============================================")
	print("\t\t🥝 " + APP_BRAND_NAME)
	print("==============================================")
	print("1. Manajemen data produk")
	print("2. Buat transaksi pelanggan")
	print("3. Lihat semua histori transaksi")
	print("4. EXIT program")
	print("==============================================")

	# Perulangan while, supaya pertanyaan berulang jika user salah input pilihan
	while True:
		try:
			navigation = int(input("Pilih menu di atas untuk melanjutkan aksi: ")) # Input untuk navigasi menu
			if navigation == 1:
				os.system('cls')
				controllers.MenuManagementProduk()
				break
			elif navigation == 2:
				os.system('cls')
				controllers.TransaksiProduk()
				break
			elif navigation == 3:
				os.system('cls')
				controllers.HistoriTransaksi()
				break
			elif navigation == 4:
				os.close
				break
			else:
				print(colored("Masukkan pilihan menu dengan benar!", "red"))
				continue
		except ValueError as err:
			print(colored("Masukkan pilihan menu dengan benar!", "red"))
