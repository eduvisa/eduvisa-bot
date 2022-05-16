from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
import members
from discord.commands import Option,slash_command
abc=None
ticketMessage = None
timeDiff=None
duration_in_minutes = None


thresholds = {
  "5" : 250,
  "10" : 510,
}
class CommandEvents(commands.Cog):
  def __init__(self,client) -> None:
      self.client=client
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    await guild.system_channel.send("Hey there, thanks for inviting me. Please set a channel using `e!setchannel <channel>` where all the communication would take place")
  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.client.user} has logged in!')
    await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="e!help"))
  @commands.Cog.listener()
  async def on_message(self,message : discord.Message):
    channel =self.client.get_channel(myBot.modmailChannelId)
    if message.author==self.client.user:
      return
    if message.guild == None:
      embed=discord.Embed(title=f"Message sent by {message.author}.",description=f"{message.content}",color=discord.Color.random())
      now=datetime.now(timezone.utc)
      timern = now.strftime("%H:%M:%S")
      embed.set_footer(text=f"Message was sent at {timern} UTC",icon_url=message.author.display_avatar)
      messageAB = await self.client.get_channel(myBot.modmailChannelId).send(embed=embed)
      await message.reply(embed=discord.Embed(title="Thank you for sending the message, someone will respond to it soon!",color=discord.Color.green()))
      myBot.current_open_queries[messageAB.id]=message.author
      print(myBot.current_open_queries)
      return
    if message.channel==channel:
      if message.reference is None:
        await message.reply(embed=discord.Embed(title="Please reply to the message you'd like to respond to",color=discord.Color.green()))
        return
      messageId = message.reference.message_id
      embed=discord.Embed(title=f"{message.author} replied to your message",description=f"{message.content}",color=discord.Color.green())
      await myBot.current_open_queries[messageId].send(embed=embed)
      await message.channel.send(embed=discord.Embed(title="Successfully responded to the member!",color=discord.Color.green()))
      return
    

    members.increaseXP(message.author, 5)
    members.increaseMessagesSent(message.author)





    

    

  @slash_command(name="ping")
  async def ping(self,ctx):
    await ctx.respond(embed=discord.Embed(title="Pong!!",description=f"{int((self.client.latency)*1000)} ms ",color=discord.Color.random()))
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
      if after.channel.id in myBot.current_session.values():
        now=datetime.now()
        timern = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"{member} has joined the vc at {timern}")
    except Exception:pass'''

def setup(client):
  client.add_cog(CommandEvents(client))