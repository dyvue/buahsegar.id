import sqlite3
conn = sqlite3.connect('./store/buahsegarid.db')
conn.execute("INSERT INTO product (kode, nama, harga) VALUES ('1000', 'Semangka', 10000)")
conn.commit()
conn.close()