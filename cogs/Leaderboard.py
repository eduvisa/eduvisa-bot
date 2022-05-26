from email.policy import default
from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
from discord.commands import Option,slash_command
import aiohttp
import members
import random

randomFooters = ["yay", "😎", "wow so cool",
                 "great job!", "meh", "yo thats sick!!"]

class Leaderboard(commands.Cog):
 def __init__(self,client) -> None:
     self.client=client
 @slash_command(name="leaderboard",description="Gives the tutor leaderboard for various categories")
 async def leaderboard(self,ctx,category:Option(str, "Category for leaderboard", required = False,default="EdCoins 🪙", choices = ["EdCoins 🪙","Volunteer Hours","Points", "Commands Used","Messages Sent","Wallet Balance","Bank Balance"]), top: Option(int, "How many top entries", required = False, default = 10, choices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])):
  if category == "Volunteer Hours":
    aaaa = ""
    bbbb = ""
    myBot.cursor.execute(
        f"SELECT username, volunteerMinutes FROM members ORDER BY volunteerMinutes DESC LIMIT {top};")
    abc = myBot.cursor.fetchall()
    if len(abc) < top:
        top = len(abc)
    for i in range(0,top):
      aaaa = str(aaaa + str(abc[i][0]))+"\n"
      hours = int((abc[i][1])/60)
      bbbb = str(bbbb + str(hours))+"\n"

    embed = discord.Embed(title=f"Top tutors", color = discord.Color.purple())
    embed.add_field(name="Username", value=f"{aaaa}",inline=True)
    embed.add_field(name="Points",value=f"{bbbb}",inline = True)
    embed.set_footer(text=":D")
    return await ctx.respond(embed=embed)
   
    
  elif category=="Commands Used":categoryc="commandsUsed"

  elif category=="EdCoins 🪙":categoryc = "netWorth"

  elif category=="Wallet Balance":categoryc="walletBalance"

  elif category=="Bank Balance":categoryc="bankBalance"

  # Getting the data from the database
  myBot.cursor.execute(f"SELECT username,{categoryc} FROM members ORDER BY {categoryc} DESC LIMIT {top};")
  names = ""
  values = ""

  data = myBot.cursor.fetchall()
  #checking if the length of the string returned is correct
  if len(data) < top: top = len(data)
  # Making the String for the embed description
  for i in range(0, top):
      names = str(names + str(data[i][0]))+"\n"
      values = str(values + str(data[i][1]))+"\n"

  # Creating the final embed
  embed = discord.Embed(title=f"The top {category}", color = discord.Color.purple())
  embed.add_field(name="Username", value=f"{names}",inline=True)
  embed.add_field(name=f"{category}",value=f"{values}",inline = True)
  embed.set_footer(text=f"{random.choice(randomFooters)}")
  members.increaseCommandsUsed(ctx)
  return await ctx.respond(embed=embed)



  



def setup(client):
 client.add_cog(Leaderboard(client))