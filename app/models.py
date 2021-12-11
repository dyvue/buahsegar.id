import uuid #UUID generator
import pandas as pd # Impor pandas untuk tampilan table
from tabulate import tabulate # Tabulate
from config.conn import conn, sqlite3 # Impor koneksi database file (config/conn.py)

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
		return True
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