import sqlite3
conn = sqlite3.connect('students.db')
cursor = conn.execute("SELECT * from STUDENT")
print(cursor.fetchall())
conn.close()