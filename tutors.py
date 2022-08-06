import sqlite3

db = sqlite3.connect("members.db")

cursor = db.cursor()

def addTutor(tutor):
    cursor.execute(f"INSERT OR IGNORE INTO tutors(tutor) VALUES('{tutor}');")
    db.commit()

def updateHours(tutor, volunteerHours):
    addTutor(tutor)
    cursor.execute(f"UPDATE tutors SET vh = vh+{volunteerHours} WHERE tutor='{tutor}';")
    db.commit()

def updatePoints(tutor, points):
    addTutor(tutor)
    cursor.execute(f"UPDATE tutors SET points = points+{points} WHERE tutor='{tutor}';")
    db.commit()
