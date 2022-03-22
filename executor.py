import sqlite3
db = sqlite3.connect("members.db")
cursor=db.cursor()

cursor.execute("ALTER TABLE members ADD netWorth INT GENERATED ALWAYS AS (bankBalance+walletBalance);")
db.commit()