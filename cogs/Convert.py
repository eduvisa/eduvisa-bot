from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
from discord.commands import Option,slash_command
import members
class MyView(discord.ui.View):
 def __init__(self,ctx,hours,tutor, tutorPoints):
     super().__init__(timeout=35)
     self.ctx=ctx
     self.tutor=tutor
     self.hours=hours
     self.tutorPoints = tutorPoints
 @discord.ui.button(label="Yes",style=discord.ButtonStyle.green,emoji = "✅")
 async def button_callback1(self,button,interaction):
  points=self.tutorPoints
  if points>=self.hours*120:
   myBot.cursor.execute(f"UPDATE members SET points = points - {self.hours*120}, volunteerMinutes = volunteerMinutes + {self.hours*60} WHERE id = {self.tutor.id};")
   myBot.db.commit()
   embed=discord.Embed(title=f"Successfully converted {self.hours*120} points into {self.hours} volunteer hours",color=discord.Color.green())
   members.increaseCommandsUsed(self.ctx)
   await interaction.response.edit_message(embed=embed,view=None)
 @discord.ui.button(label="No", style= discord.ButtonStyle.danger,emoji = "❌")
 async def buttoncallback(self,button,interaction):
  embed=discord.Embed(title=f"Successfully cancelled the conversion!",color=discord.Color.green())
  await interaction.response.edit_message(embed=embed,view=None)



class Convert(commands.Cog):
  def __init__(self,client) -> None:
      self.client=client

  @slash_command(name="convert",description="Convert some of your points into volunteer hours")
  @commands.has_any_role(883840894418182165,843466315125227550,745179262482382969,941949149291626536)
  async def convert1(self,ctx,tutor:Option(discord.Member,"The tutor to convert the points for",required=True),hours:Option(str,"Amount of hours to convert from points",required=True,choices = ["max","1","2","3","4","5","6","7","8","9","10"])):
    await ctx.defer()
    points = members.getValue("points",tutor.id, tutor, False)

    if hours=="max":
      hours = points // 120
      embed=discord.Embed(title="Confirmation",description = f"Are you sure you want to spend {hours*120} points to get {hours} volunteer hours?",color=discord.Color.purple())
      await ctx.respond(embed=embed,view=MyView(ctx,hours,tutor, points))
      return
    else:
      hours = int(hours)


    if hours<=0:
      embed=discord.Embed(title="I don't think you can do that",color=discord.Color.purple())
      embed.set_footer(text="🙄")
      await ctx.respond(embed=embed)
      return
    elif hours>points // 120:
      return await ctx.respond(embed=discord.Embed(title=f"The tutor doesn't have the required points to achieve {hours} hours", description = f"Tutor Points : **{points}**\n Points Required : {hours * 120}", color = discord.Color.random()))
    
    embed=discord.Embed(title="Confirmation",description = f"Are you sure you want to spend {hours*120} points to get {hours} volunteer hours?",color=discord.Color.purple())
    await ctx.respond(embed=embed,view=MyView(ctx,hours,tutor, points))
    







def setup(client):
 client.add_cog(Convert(client))