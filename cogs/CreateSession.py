from discord.ext import commands
import discord
import manager
import main
from datetime import datetime, timezone
import members

from discord.commands import Option, slash_command

botRoleId = 979369483258953809
tutoringChannel = main.client.get_channel(979444728183545916)

class MyView(discord.ui.View):
    def __init__(self, ctx, tc, client, student):
        super().__init__(timeout=0)
        self.ctx = ctx
        self.channel = tc
        self.client = client
        self.student = student


    @discord.ui.button(label="END SESSION ❌", style = discord.ButtonStyle.primary)
    async def buttoncallback(self, button, interaction):
        if self.channel.id in manager.active_sessions.keys():
          
            try:
                vc =self.client.get_channel(manager.active_sessions[self.channel.id])
                await vc.delete()
            except Exception as e:print(e)
    
            manager.active_sessions.pop(self.channel.id)
            timeCreated= self.channel.created_at
            timeEnded = datetime.now(timezone.utc)
            duration = timeEnded-timeCreated
            duration_in_minutes = divmod(duration.total_seconds(),60)[0]
            members.updateHours(self.ctx.author.id, self.ctx.author, int(duration_in_minutes))
            tutoringChannel = self.channel.guild.get_channel(979444728183545916)
            await self.channel.delete()


            await tutoringChannel.send(embed = discord.Embed(title = f"{self.ctx.author} just ended a tutoring session", description = f"Tutor : {self.ctx.author} \n\n Student : {self.student} \n\n Session Duration: {duration_in_minutes} minutes", color = discord.Color.nitro_pink()))
            await self.ctx.send(embed = discord.Embed(title = "Your session successfully ended and your volunteer hours have been recorded", color = discord.Color.green()))

    async def interaction_check(self, interaction:discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Nope, you cant do that! Only the tutor can do that! <:angrycry:800398476969377822>", ephemeral=True)
            return False
        else:
            return True      
        


            

            

class CreateSession(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @slash_command(name="createsession", description="Create a private session with a student!")
    @commands.has_any_role(883840894418182165, 843466315125227550, 745179262482382969, 941949149291626536)
    async def createsession(self, ctx, member:Option(discord.Member, "Student that you would like to create a session with", required = True)):

        botRole = ctx.guild.get_role(botRoleId)
        
        category = discord.utils.get(ctx.guild.categories, id=986411485486006302)
        vc = await ctx.guild.create_voice_channel(category=category, name=f"{ctx.author.name}'s Voice Channel", overwrites={ctx.author: discord.PermissionOverwrite(view_channel=True, connect=True), member: discord.PermissionOverwrite(view_channel=True, connect=True), ctx.guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False), botRole: discord.PermissionOverwrite(view_channel=True,connect=True)}, position=0)
        tc = await ctx.guild.create_text_channel(category=category, name=f"Tutoring Session", overwrites={ctx.author: discord.PermissionOverwrite(view_channel=True), member: discord.PermissionOverwrite(view_channel=True), ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False), botRole: discord.PermissionOverwrite(view_channel=True)}, position=1)

        manager.active_sessions[tc.id] = vc.id
        


        await ctx.respond(embed=discord.Embed(title="Success!", description=f"Successfully created a private session between {ctx.author.mention} and {member.mention}\nIt can be found at - <#{tc.id}>", color=discord.Color.green()))

        await tc.send(f"{ctx.author.mention}\n{member.mention}", embed = discord.Embed(title = "Have a fun class <3", description = f"I hope you have a fun session at <#{vc.id}>, also, when you're done, press the button below to end the session.", color=discord.Color.green()), view = MyView(ctx, tc, self.client, member))




def setup(client):
    client.add_cog(CreateSession(client))
