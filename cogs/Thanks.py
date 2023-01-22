from discord.ext import commands
import discord
import members
from discord.commands import Option, slash_command
class Thanks(commands.Cog):
    # Initialize
    def __init__(self, client) -> None:
        self.client = client

    # Begin slash command
    @slash_command(name="thank",description = "Thank a member")
    #Define command and parameters
    async def thank1(self,ctx,member:Option(discord.Member,"Member to thank",required=True),reason:Option(str,"Reason for thanking the member",required=True)):
        await ctx.defer()
        #Create the embed
        embed=discord.Embed(title=f"{member} was thanked", description = f"The tutor {member} was thanked in {ctx.channel.mention} by {ctx.author}.\n**REASON : {reason}** [Go to message]({ctx.message.jump_url})",color=discord.Color.nitro_pink())
        #Send the embed
        await ctx.guild.get_channel(members.thanksChannel).send(embed=embed)


        await ctx.send(embed=discord.Embed(title="You're welcome ✔️", color=discord.Color.green))



def setup(client):
    client.add_cog(Thanks(client))