from discord.ext import commands
import discord

#import members
from discord.commands import Option, slash_command
abc = None
ticketMessage = None
timeDiff = None
duration_in_minutes = None


class CommandEvents(commands.Cog):
  def __init__(self, client) -> None:
      self.client = client
    
#   @commands.Cog.listener()
#   async def on_guild_join(self, guild):
#     await guild.system_channel.send("Hey there, thanks for inviting me. Please set a channel using `e!setchannel <channel>` where all the communication would take place")
    
  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.client.user} has logged in!')
    await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="e!help"))
  @commands.Cog.listener()
  async def on_message(self, message : discord.Message):
      cookiechannel = self.client.get_channel(765600086825893909)
      studentapps = self.client.get_channel(999998980006092861)
      disboard = self.client.get_user(302050872383242240)
      zapier = self.client.get_user(1000094690697285714)
      if message.author == self.client.user:
          return
      if message.content == "<@942341036418695198>":
          await message.channel.send(embed=discord.Embed(title="WHOMST HAS AWAKEN ME!", description="I don't do prefix commands 💀\n\n Only `/` commands work with me!!", color = discord.Color.green()))
      if message.channel == cookiechannel and message.author == disboard:
          await message.add_reaction("🍪")
      if message.channel == studentapps and message.author == zapier:
          await studentapps.send("<@&799910046631723028>")
        
          
#   @commands.Cog.listener()
#   async def on_message(self, message: discord.Message):
#     channel = self.client.get_channel(main.modmailChannelId)
#     if message.author == self.client.user:
#       return
#     if message.guild == None:
#       embed = discord.Embed(title=f"Message sent by {message.author}.",
#                             description=f"{message.content}", color=discord.Color.random())
#       now = datetime.now(timezone.utc)
#       timern = now.strftime("%H:%M:%S")
#       embed.set_footer(
#           text=f"Message was sent at {timern} UTC", icon_url=message.author.display_avatar)
#       messageAB = await self.client.get_channel(main.modmailChannelId).send(embed=embed)
#       await message.reply(embed=discord.Embed(title="Thank you for sending the message, someone will respond to it soon!", color=discord.Color.green()))
#       main.current_open_queries[messageAB.id] = message.author
#       print(main.current_open_queries)
#       return
#     if message.channel == channel:
#       if message.reference is None:
#         await message.reply(embed=discord.Embed(title="Please reply to the message you'd like to respond to", color=discord.Color.green()))
#         return
#       messageId = message.reference.message_id
#       embed = discord.Embed(title=f"{message.author} replied to your message",
#                             description=f"{message.content}", color=discord.Color.green())
#       await main.current_open_queries[messageId].send(embed=embed)
#       await message.channel.send(embed=discord.Embed(title="Successfully responded to the member!", color=discord.Color.green()))
#       return

#     members.increaseMessagesSent(message.author)

  @slash_command(name="ping", description="You know the thing you blame when you get an L at Fornite? yeah, me too")
  async def ping(self, ctx):
    await ctx.respond(embed=discord.Embed(title="Pong!!", description=f"{int((self.client.latency)*1000)} ms ", color=discord.Color.random()))

  ''' @commands.command()
  async def createticket(self,ctx):
    ticketMessage = await ctx.send("Please react to the message below")
    print(ticketMessage)
    await ticketMessage.add_reaction("‼")
  @commands.Cog.listener()
  async def on_voice_state_update(self,member,before,after):
    if len(after.channel.members)==2:
      print("Got till here!")
    try:
      if after.channel.id in main.current_session.values():
        now=datetime.now()
        timern = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"{member} has joined the vc at {timern}")
    except Exception:pass'''


def setup(client):
  client.add_cog(CommandEvents(client))
