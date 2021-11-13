import sqlite3
conn = sqlite3.connect('./store/buahsegarid.db')
conn.execute("DELETE from product")
conn.commit()
cursor = conn.execute("SELECT * from product")
print(cursor.fetchall())
conn.close()