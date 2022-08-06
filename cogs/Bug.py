from discord.ext import commands
import discord

from discord.commands import Option,slash_command
import members
channelId = 942689366483013642

class Report(commands.Cog):
  def __init__(self,client):
    self.client=client


  # @commands.command(name="report",aliases=[" report","Report"," Report","bug"," bug","Bug"," Bug","REPORT"," REPORT","BUG"," BUG"])
  # async def report(self,ctx,*,bug):
  #   await ctx.send(embed=discord.Embed(title="Successfully reported the bug <a:blobdance:853873081571344394>",description="Our developers (okay there's only one, **Achintya#7777**) will get back to you soon.",color=discord.Color.nitro_pink()))
  #   channel = await ctx.guild.fetch_channel(channelId)
  #   await channel.send(embed=discord.Embed(title=f"{ctx.author} reported a bug",description=f"{bug}",color=discord.Color.dark_red()))
  @slash_command(name="bug", description="Report a bug, get EdCoins as a reward hehe!")
  async def report(self,ctx,bug:Option(str,"What the bug is",required=True)):
    await ctx.respond(embed=discord.Embed(title="Successfully reported the bug",description="Our developers (okay there's only one, **Achintya#4448**) will get back to you soon!",color=discord.Color.nitro_pink()))
    channel = await ctx.guild.fetch_channel(channelId)
    await channel.send(embed=discord.Embed(title=f"{ctx.author} reported a bug",description=f"{bug}",color=discord.Color.dark_red()))
    members.increaseCommandsUsed(ctx)




def setup(client):
  client.add_cog(Report(client))