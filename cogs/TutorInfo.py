from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
from discord.commands import Option,slash_command

class TutorInfo(commands.Cog):
 def __init__(self,client) -> None:
     self.client=client
 
 # @commands.command(aliases=["ti"])
 # async def tutorinfo(self,ctx,member:discord.Member=None):
 #  if member == None:
 #   await ctx.reply(embed=discord.Embed(title="Please mention the tutor to get info about",color=discord.Color.purple()))
 #   return
 #  myBot.cursor.execute(f"INSERT OR IGNORE INTO tutorInfo(tutorId,tutorName,tutorPoints,tutorWorkingHours) VALUES({member.id},'{member}',0,0);") 
 #  myBot.db.commit()
 #  myBot.cursor.execute(f"SELECT tutorWorkingHours,tutorPoints FROM tutorInfo WHERE tutorId = {member.id};")
 #  result = myBot.cursor.fetchone()
 #  workingHours = result[0]/60
 #  points=result[1]
 #  embed = discord.Embed(title=f"{member}",color=discord.Color.purple())
 #  embed.add_field(name="Points",value=f"{points}")
 #  embed.add_field(name="Volunteer Hours",value = f"{int(workingHours)}",inline=False)
 #  await ctx.send(embed=embed)
 @slash_command(name="tutorinfo",description="Returns info about a tutor")
 async def tutorinfo1(self,ctx,member:Option(discord.Member,"The tutor to get info about", required=True)):
  await ctx.defer()
  myBot.cursor.execute(f"INSERT OR IGNORE INTO tutorInfo(tutorId,tutorName,tutorPoints,tutorWorkingHours) VALUES({member.id},'{member}',0,0);") 
  myBot.db.commit()
  myBot.cursor.execute(f"SELECT tutorWorkingHours,tutorPoints FROM tutorInfo WHERE tutorId = {member.id};")
  result = myBot.cursor.fetchone()
  workingHours = result[0]/60
  points=result[1]
  embed = discord.Embed(title=f"{member.displayName}",color=discord.Color.random())
  embed.add_field(name="Points",value=f"{points}")
  embed.add_field(name="Volunteer Hours",value = f"{int(workingHours)}",inline=False)
  await ctx.respond(embed=embed)



def setup(client):
 client.add_cog(TutorInfo(client))