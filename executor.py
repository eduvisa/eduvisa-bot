import sqlite3
db = sqlite3.connect("members.db")
cursor=db.cursor()

cursor.execute("CREATE TABLE economy (id BIGINT PRIMARY KEY, name VARCHAR, netWorth INT, walletBalance INT, bankBalance INT, dailyStreak INT, FOREIGN KEY (name) REFERENCES members (name), FOREIGN KEY (netWorth) REFERENCES members (netWorth), FOREIGN KEY (walletBalance) REFERENCES members (walletBalance), FOREIGN KEY (bankBalance) REFERENCES members (bankBalance));")
db.commit()