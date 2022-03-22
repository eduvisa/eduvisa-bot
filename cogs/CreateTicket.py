from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
import os
from discord.commands import Option,slash_command
import members
ticketClaimers={}
class MyView1(discord.ui.View):
  def __init__(self,channel,member):
      super().__init__(timeout=0)
      self.channel=channel
      self.member=member
  @discord.ui.button(label="Close",style=discord.ButtonStyle.danger,emoji="❌")
  async def buttoncallback(self,button,interaction):
    try:
      f = open("history.txt", "w")
      async for message in self.channel.history(limit=None, oldest_first=True):
        if message.content == "" or message.content == None:
          continue
        line = f"{message.author.name} | {message.content}"
        f.write("\n")
        f.write(line)
      f.close()
      file = discord.File("history.txt")
      embed=discord.Embed(title="Successfully closed the ticket",description="**HERE'S A COPY OF THE MESSAGE HISTROY**",color=discord.Color.green())
      embed.set_footer(text="hope we resolved your query :D")
      try:
        await ticketClaimers[interaction.user].send(embed=embed)
        await ticketClaimers[interaction.user].send(file=file)
        ticketClaimers.pop(interaction.user)
      except Exception as getgood:
        try:
          await interaction.user.send(embed=embed)
          await interaction.user.send(file=file)
        except Exception:pass
        print(getgood)

      
      os.remove("history.txt")
      await self.channel.delete()
    except:self.channel.delete()
  @discord.ui.button(label="Claim",style=discord.ButtonStyle.primary,emoji = "⏺")
  async def butcallback(self,button,interaction):
    role = self.channel.guild.get_role(942342850593558532)
    #modRole=self.ctx.guild.get_role(843466315125227550)
    #adminRole=self.ctx.guild.get_role(883840894418182165)
    testAdminRole = self.channel.guild.get_role(941949149291626536)
    testModRole= self.channel.guild.get_role(943394759471431710)
    if testAdminRole not in interaction.user.roles or testModRole not in interaction.user.roles:
      await interaction.response.send_message("Only a mod/admin can claim a ticket",ephemeral=True)
    else:
      await self.channel.set_permissions(testModRole, view_channel=False)
      await self.channel.set_permissions(interaction.user,view_channel=True) 
      ticketClaimers[interaction.user] = self.member
      await interaction.response.send_message("Successfully claimed the ticket!",ephemeral=True)


class MyView(discord.ui.View):
  def __init__(self,ctx,client):
      super().__init__(timeout=0)
      self.ctx=ctx
      self.client=client
  
  @discord.ui.button(label='CREATE TICKET!',style=discord.ButtonStyle.primary,emoji="‼")
  async def button_callback(self,button,interaction):
    role = self.ctx.guild.get_role(942342850593558532)
    #modRole=self.ctx.guild.get_role(843466315125227550)
    #adminRole=self.ctx.guild.get_role(883840894418182165)
    testAdminRole = self.ctx.guild.get_role(941949149291626536)
    testModRole= self.ctx.guild.get_role(943394759471431710)
    channel = await self.ctx.guild.create_text_channel(name=f"{interaction.user.name} ticket",overwrites={interaction.user:discord.PermissionOverwrite(view_channel=True),role:discord.PermissionOverwrite(view_channel=True),testModRole:discord.PermissionOverwrite(view_channel=True),testAdminRole:discord.PermissionOverwrite(view_channel=True)},position=0)
    embed=discord.Embed(title="Ticket Created",description="Successfully created a ticket\nHelp will be with you soon\n**PLEASE WRITE YOUR QUERY IN THE CHANNEL**",color=discord.Color.purple())
    await channel.send(embed=embed,view=MyView1(channel,interaction.user))
    await interaction.response.send_message(f"I have created a ticket, it can be found at <#{channel.id}>",ephemeral=True)
    members.increaseCommandsUsed(self.ctx)
    

class CreateTicket(commands.Cog):
 def __init__(self,client) -> None:
    self.client=client

@slash_command()
async def createticket(self, ctx):
  await ctx.defer()
  embed=discord.Embed(title="CREATE TICKET",description="Click the button below to create a ticket and a mod/admin will respond to it soon!",color=discord.Color.nitro_pink())
  embed.set_footer(icon_url=self.client.user.display_avatar,text="yep, that big blue button")
  await ctx.respond(embed=embed,view=MyView(ctx,self.client))
    


def setup(client):
 client.add_cog(CreateTicket(client))