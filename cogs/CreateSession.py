from unicodedata import category
from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
from discord.commands import Option,slash_command
import members
sessionLogs = 942615772700766208


class MyView(discord.ui.View):
  def __init__(self,ctx,channel,client, student):
    super().__init__(timeout=0)
    self.ctx=ctx
    self.channel = channel
    self.client = client
    self.student = student


  @discord.ui.button(label="End Session",style=discord.ButtonStyle.primary,emoji="❌")
  async def buttoncallback1(self,button,interaction):
    if self.channel.id in myBot.current_session:
      category=self.channel.category
      try:
        vc =self.client.get_channel(myBot.current_session[self.channel.id])
        await vc.delete()
      except Exception:pass
      myBot.current_session.pop(self.channel.id)
      timeCreated= self.channel.created_at
      timeEnded = datetime.now(timezone.utc)
      duration = timeEnded-timeCreated
      duration_in_mintues = divmod(duration.total_seconds(),60)[0]

      members.updateValue(self.ctx.author.id, self.ctx.author, "volunteerMinutes", f"volunteerMinutes+{duration_in_mintues}")
      await self.channel.delete()
      await category.delete()
      try:
        embed=discord.Embed(title=f"Successfully ended the session! It lasted for {int(duration_in_mintues)} minutes!",color=discord.Color.green())
        await self.ctx.author.send(embed=embed)
        await self.ctx.guild.get_channel(sessionLogs).send(embed=discord.Embed(title=f"{self.ctx.author} just ended a session!", description=f"Student: {self.student}\n Duration `{int(duration_in_mintues)}"))
      except Exception as getgood:
        await self.ctx.guild.get_channel(sessionLogs).send(embed=discord.Embed(title=f"{self.ctx.author} just ended a session!", description=f"Student: {self.student}\n Duration `{int(duration_in_mintues)}"))

        print(getgood)
    else:pass

  async def interaction_check(self, interaction:discord.Interaction) -> bool:
    if interaction.user != self.ctx.author:
        await interaction.response.send_message("Nope, you cant do that! Only the tutor can end the session.", ephemeral=True)
        return False
    else:
        return True

class CreateSession(commands.Cog):

  def __init__(self,client):
      self.client=client


  @slash_command(name="createsession",description="Create a private session with a member!")
  @commands.has_any_role(883840894418182165,843466315125227550,745179262482382969,941949149291626536)
  async def createsession1(self,ctx, member:Option(discord.Member,"Member to make session with",required=True)):
    await ctx.defer()

    category = await ctx.guild.create_category(name=f"{ctx.author.name} is tutoring",position=0,overwrites={ctx.author:discord.PermissionOverwrite(view_channel=True),member:discord.PermissionOverwrite(view_channel=True),ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False)})

    vc = await ctx.guild.create_voice_channel(category=category,name=f"{ctx.author.name}'s Voice Channel",overwrites={ctx.author:discord.PermissionOverwrite(view_channel=True),member:discord.PermissionOverwrite(view_channel=True),ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False)},position=0)

    tc = await ctx.guild.create_text_channel(category=category,name=f"Tutoring Session",overwrites={ctx.author:discord.PermissionOverwrite(view_channel=True),member:discord.PermissionOverwrite(view_channel=True),ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False)},position=1)
    myBot.current_session[tc.id] = vc.id
    view=MyView(ctx,tc,self.client)

    await ctx.respond(embed=discord.Embed(title="Success!",description=f"Successfully created a private session between {ctx.author.mention} and {member.mention}\nIt can be found at - <#{tc.id}>",color=discord.Color.green()))

    await tc.send(f"{ctx.author.mention}\n{member.mention}",embed=discord.Embed(title="Voice Chat Created",description=f"Created a private voice chat between {ctx.author.mention} and {member.mention}.\nIt can be found at <#{vc.id}>\n To end the session, click the button below or type `e!sessionend`!",color=discord.Color.purple()),view=view)

    myBot.assignedStudent[ctx.author] = member
    members.increaseCommandsUsed(ctx)



def setup(client):
 client.add_cog(CreateSession(client))
 