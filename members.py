import discord
import sqlite3
db = sqlite3.connect("members.db")
cursor=db.cursor()
thanksChannel = 1050825390941278249


def addMember(member, membername):
    cursor.execute(f"INSERT OR IGNORE INTO members(id, username) VALUES({member},'{membername}');")
    db.commit()
def markAsTutor(member, membername):
    addMember(member, membername)
    cursor.execute(f"UPDATE members SET isTutor=1 WHERE id={member};")
def updateValue(id, name, field, value):
    addMember(id, name)
    cursor.execute(f"UPDATE members SET {field} = {value} WHERE id = {id};")
    db.commit()
def updateHours(tutorId, tutor, vh):
    addMember(tutorId, tutor)
    cursor.execute(f"UPDATE members SET isTutor=1 WHERE id={tutorId};")
    cursor.execute(f"UPDATE members SET volunteerMinutes = volunteerMinutes+{vh} WHERE id={tutorId};")
    db.commit()
def increaseCommandsUsed(ctx):
    addMember(ctx.author.id, ctx.author)
    cursor.execute(f"UPDATE members SET commandsUsed = commandsUsed + 1 WHERE id={ctx.author.id};")
    db.commit()

def addPoints(id:int,name,points):
    addMember(id, name)
    updateValue(id, name, "points", f"points+{points}")

def getValue(valueName, id, name, fetchmany:bool):
    addMember(id, name)
    cursor.execute(f"SELECT {valueName} from members WHERE id = {id};")
    #print(f"SELECT {valueName} from members WHERE id = {id};")
    if fetchmany:
        return cursor.fetchall()[0]
    else:
        return cursor.fetchone()[0]


def increaseMessagesSent(member):
    addRanker(member)
    cursor.execute(
        f"UPDATE ranks SET messagesSent = messagesSent + 1 WHERE user={member};")
    db.commit()


