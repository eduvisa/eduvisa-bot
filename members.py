import discord
import sqlite3
db = sqlite3.connect("members.db")
cursor=db.cursor()

def addRanker(member:discord.Member):
    cursor.execute(f"INSERT OR IGNORE INTO ranks(user) VALUES('{member}');")
    db.commit()


def check(member : discord.Member) -> bool:
    cursor.execute(f"SELECT xp FROM ranks WHERE user='{member}';")
    [currentXP] = cursor.fetchone()

    cursor.execute(f"SELECT threshold FROM ranks WHERE user='{member}';")

    [currentThreshold] = cursor.fetchone
    if currentXP >= currentThreshold:
        return True
    else: return False


def addMember(member, membername):
    cursor.execute(f"INSERT OR IGNORE INTO members(id, username) VALUES({member},'{membername}');")
    db.commit()
    
def updateValue(id, name, field, value):
    addMember(id, name)
    cursor.execute(f"UPDATE members SET {field} = {value} WHERE id = {id};")
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

def increaseXP(member, value):
    addRanker(member)
    cursor.execute(f"UPDATE ranks SET xp = xp + {value} WHERE user = '{member}';")
    db.commit()


def getXP(valueName, id, name, fetchmany: bool):
    cursor.execute(f"SELECT {valueName} from ranks WHERE user = {name};")
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


