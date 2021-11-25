from conn import conn

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS produk")
query = """CREATE TABLE produk(
	kode INTEGER PRIMARY KEY,
	nama VARCHAR(50) NOT NULL, 
	harga DECIMAL(10,2) NOT NULL
)"""
cursor.execute(query)

conn.execute("INSERT INTO produk (kode, nama, harga) VALUES (1000, 'Apel', 35000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Alpukat', 35000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Blimbing', 15000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Jambu', 26000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Jeruk', 5000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Durian', 20000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Kelengkeng', 35000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Mangga', 15000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Melon', 10000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Nanas', 10000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Nangka', 10000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Buah Naga', 10000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Pisang Monyet', 10000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Pisang Ambon', 12000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Pisang Batu', 11000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Rambutan', 25000)")
conn.execute("INSERT INTO produk (nama, harga) VALUES ('Salak', 20000)")
conn.commit()

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS transaksi")
query = """CREATE TABLE transaksi(
	kode VARCHAR(36) PRIMARY KEY,
	nama_kasir VARCHAR(50) NOT NULL, 
	total DECIMAL(10,2) NOT NULL,
	bayar DECIMAL(10,2) NOT NULL,
	kembali DECIMAL(10,2) NOT NULL,
	tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""
cursor.execute(query)

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS transaksi_produk")
query = """CREATE TABLE transaksi_produk(
	kode INTEGER PRIMARY KEY,
	transaksi_id VARCHAR(36) NOT NULL, 
	produk_id VARCHAR(10) NOT NULL,
	jumlah INTEGER NOT NULL,
	total DECIMAL(10,2) NOT NULL
)"""
cursor.execute(query)