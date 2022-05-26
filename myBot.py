import dotenv
from keep_alive import keep_alive
dotenv.load_dotenv()
import os
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import sqlite3


client = commands.Bot(command_prefix="e!", intents=discord.Intents.all(),debug_guilds=[819224446727487518,707278018405466253])

client.remove_command("help")
current_session = {}
guildLogChannels = {}
assignedStudent = {}
guildThankChannels={}
logChannel = None
db = sqlite3.connect("members.db")
ticketMessage = None
cursor=db.cursor()
abc=None
modmailChannelId = 940828313868435516
feedbackChannelId = 942615772700766208
feedbackChannel = client.get_channel(feedbackChannelId)
timeDiff=None
duration_in_minutes = None
current_open_queries={}

@slash_command()
async def help(ctx,command:Option(str,"Command you need help with", required=False, choices=["createsession","sessionend","setchannel","leaderboard","tutorinfo","convert","award","music"])):
    if command=="createsession":
      embed = discord.Embed(title="Create Session",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!createsession <member>```",inline=False)
      embed.add_field(name="Attributes",value="```member: Member to create session with```",inline=False)
      embed.add_field(name="Aliases",value="```cs```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command=="sessionend":
      embed = discord.Embed(title="End Session",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!sessionend```",inline=False)
      embed.add_field(name="Attributes",value="```None```",inline=False)
      embed.add_field(name="Aliases",value="```se```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command=="setchannel":
      embed = discord.Embed(title="Set Channel",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!setchannel <channel>```",inline=False)
      embed.add_field(name="Attributes",value="```channel: Channel to set for logs/communication```",inline=False)
      embed.add_field(name="Aliases",value="```sc```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command=="leaderboard":
      embed = discord.Embed(title="Leaderboard",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!leaderboard <category> <top:Optional>```",inline=False)
      embed.add_field(name="Attributes",value="```category: Category for the leaderboard, Current categories are - \n    1. Volunteer hours(vh)\n    2. Points(p)\ntop:Top entries, default is 10```",inline=False)
      embed.add_field(name="Aliases",value="```lb```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command=="tutorinfo":
      embed = discord.Embed(title="Tutor Info",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!tutorinfo <tutor>```",inline=False)
      embed.add_field(name="Attributes",value="tutor:Tutor to get info about",inline=False)
      embed.add_field(name="Aliases",value="```ti```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command == "convert":
      embed = discord.Embed(title="Convert",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!convert <tutor> <hours>```",inline=False)
      embed.add_field(name="Attributes",value="```tutor:The tutor to convert points for\nhours:Number of hours to get converted into(max means the maximum hours that can be converted```",inline=False)
      embed.add_field(name="Aliases",value="```None```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command=="award":
      embed = discord.Embed(title="Award",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!award <tutor> <points>```",inline=False)
      embed.add_field(name="Attributes",value="```tutor:The tutor to award the points\npoints:Number of points to award```",inline=False)
      embed.add_field(name="Aliases",value="```None```",inline=False)
      await ctx.send(embed=embed)
      return
    elif command=="music":
      embed = discord.Embed(title="Music Commands",color=discord.Color.dark_red())
      embed.add_field(name="Usage:",value="```e!award <tutor> <points>```",inline=False)
      embed.add_field(name="Attributes",value="```tutor:The tutor to award the points\npoints:Number of points to award```",inline=False)
      embed.add_field(name="Aliases",value="```None```",inline=False)
      await ctx.send(embed=embed)


    embed = discord.Embed(title="Help Command",description="Hey There, I am **EduVisa Bot(e!)**. Following are my commands: ",color=discord.Color.dark_red())
    embed.add_field(name="`e!createsession`", value="Creates a tutoring session with a member")
    embed.add_field(name="`e!sessionend`",value="Ends and ongoing session with the member")
    embed.add_field(name="`e!setchannel`",value="Sets a channel for all logs/communication to take place.")
    embed.add_field(name="`e!leaderboard`",value="Get the leaderboard of tutors")
    embed.add_field(name="`e!tutorinfo`",value="Gives you info about the tutor")
    embed.add_field(name="`e!convert`",value = "Convert some of your points into volunteer hours")
    embed.add_field(name="`e!award`",value="Award someone points if they've been good")
    embed.add_field(name="Note",value="For additional help on any command, do `e!help <commandname>`",inline=False)
    embed.set_footer(text="i was developed by Achintya#7777",icon_url=client.user.display_avatar)
    await ctx.send(embed=embed)



@client.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.MissingAnyRole):
    try:
      await ctx.author.send("You do not have sufficient roles/permissions to use this command")
      return
    except Exception:
      await ctx.send("You do not have sufficient roles/permissions to use this command")
      return
  else:print(error)
@client.event
async def on_application_command_error(ctx,error):
  if error==commands.errors.MissingAnyRole:
    try:
      await ctx.author.send("You do not have sufficient roles/permissions to use this command")
      return
    except Exception:
      await ctx.send("You do not have sufficient roles/permissions to use this command")
      return
  else:pass

lst = [f for f in os.listdir("cogs/") if os.path.isfile(os.path.join("cogs/", f))]
no_py = [s.replace('.py', '') for s in lst]
startup_extensions = ["cogs." + no_py for no_py in no_py]
try:
  for cogs in startup_extensions:
    client.load_extension(cogs)  # Startup all cogs

    print(f"Loaded {cogs}")

except Exception as getgood:
  print(getgood)
keep_alive()
client.run(os.environ['TOKEN'])