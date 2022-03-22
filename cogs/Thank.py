from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
from discord.commands import Option,slash_command

class Thank(commands.Cog):
 def __init__(self,client):
     self.client=client
 @commands.command()
 async def thank(self,ctx,member:discord.Member=None,*,reason:str=None):
  if member==None:
    await ctx.reply(embed=discord.Embed(title="Please mention the tutor/member to thank",color=discord.Color.purple()))
    return
  if reason == None:
    await ctx.reply(embed=discord.Embed(title="Please mention the reason for thanking the tutor/member",color=discord.Color.purple()))
    return
  try:
   embed=discord.Embed(title=f"{member} was thanked", description = f"The tutor {member} was thanked in {ctx.channel.mention} by {ctx.author}.\n**REASON : {reason}**",color=discord.Color.nitro_pink())
   await myBot.guildThankChannels[ctx.guild.id].send(embed=embed)
  except Exception:
   embed=discord.Embed(title=f"{member} was thanked", description = f"The tutor {member} was thanked in {ctx.channel.mention} by {ctx.author}.\n**REASON : {reason}**",color=discord.Color.nitro_pink())
   embed.set_footer(text="don't want this message sent here? try doing e!setthankchannel <channel> to change the thank notifications channel")
   await ctx.guild.system_channel.send(embed=embed)
  
  embed=discord.Embed(title=f"Successfully thanked {member}!", color = discord.Color.green())

  
  await ctx.send(embed=embed)

 @slash_command(name="thank",description = "Thank a tutor")
 async def thank1(self,ctx,member:Option(discord.Member,"Tutor to thank",required=True),reason:Option(str,"Reason for thanking the tutor",required=True)):
  await ctx.defer()
  try:
   embed=discord.Embed(title=f"{member} was thanked", description = f"The tutor {member} was thanked in {ctx.channel.mention} by {ctx.author}.\n**REASON : {reason}**",color=discord.Color.nitro_pink())
   await myBot.guildThankChannels[ctx.guild.id].send(embed=embed)
  except Exception:
   embed=discord.Embed(title=f"{member} was thanked", description = f"The tutor {member} was thanked in {ctx.channel.mention} by {ctx.author}.\n**REASON : {reason}**",color=discord.Color.nitro_pink())
   embed.set_footer(text="don't want this message sent here? try doing e!setthankchannel <channel> to change the thank notifications channel")
   await ctx.guild.system_channel.send(embed=embed)
  
  embed=discord.Embed(title=f"Successfully thanked {member}!", color = discord.Color.green())
  
  await ctx.respond(embed=embed)

def setup(client):
 client.add_cog(Thank(client))