import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import sqlite3



db = sqlite3.connect("members.db")
cursor = db.cursor()
client = commands.Bot(command_prefix="e!",
                      intents=discord.Intents.all(),
                      debug_guilds=[819224446727487518, 707278018405466253])

activeSessions = {}
client.remove_command("help")


@client.command()
async def ban(ctx, member):
    await ctx.reply("no.")


@client.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.MissingAnyRole):
      await ctx.send("You do not have sufficient roles/permissions to use this command")
      return
  
      
@client.event
async def on_application_command_error(ctx,error):
  if isinstance(error, commands.MissingAnyRole):
      await ctx.send("You do not have sufficient roles/permissions to use this command")
      return
  





lst = [
    f for f in os.listdir("cogs/") if os.path.isfile(os.path.join("cogs/", f))
]
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
