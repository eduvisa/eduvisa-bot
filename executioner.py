import sqlite3

db = sqlite3.connect('members.db')
cursor = db.cursor()

cursor.execute("UPDATE members SET volunteerMinutes=volunteerMinutes+75 WHERE id=652626688928383006;")
# cursor.execute("SELECT volunteerMinutes FROM members WHERE id=516132835502063616;")
# data = cursor.fetchone()[0]
# print(data)
db.commit()