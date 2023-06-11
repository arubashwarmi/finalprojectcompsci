import sqlite3

con = sqlite3.connect("gradebook.db")

cur = con.cursor()

result = cur.execute("SELECT * FROM teachers")

print(result.fetchone())
