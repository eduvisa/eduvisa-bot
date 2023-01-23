from discord.ext import commands
import discord
from discord.commands import Option,slash_command
import members
donation_link = "https://www.paypal.com/paypalme/eduvisa"

class Donate(commands.Cog):
    def __init__(self,client):
        self.client=client

    @slash_command(name="donate",description="Donate to EduVisa! ")
    async def donate1(self,ctx):
        global button2
        button2 = discord.ui.Button(label=f"Donate!", url=f"{donation_link}")
        view = discord.ui.View(button2)
        return await ctx.respond(embed=discord.Embed(title=f"Here's Our Donation Page",color=discord.Color.nitro_pink()),view=view)


def setup(client):
  client.add_cog(Donate(client))
    
    
    