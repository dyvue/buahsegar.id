from conn import conn

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS product")
query = """CREATE TABLE product(
	kode INTEGER PRIMARY KEY,
	nama VARCHAR(50) NOT NULL, 
	harga DECIMAL(10,2) NOT NULL
)"""
cursor.execute(query)

conn.execute("INSERT INTO product (kode, nama, harga) VALUES (1000, 'Apel', 35000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Alpukat', 35000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Blimbing', 15000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Jambu', 26000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Jeruk', 5000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Durian', 20000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Kelengkeng', 35000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Mangga', 15000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Melon', 10000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Nanas', 10000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Nangka', 10000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Buah Naga', 10000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Pisang Monyet', 10000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Pisang Ambon', 12000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Pisang Batu', 11000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Rambutan', 25000)")
conn.execute("INSERT INTO product (nama, harga) VALUES ('Salak', 20000)")
conn.commit()