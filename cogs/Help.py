from discord.ext import commands
import discord
from discord.commands import Option,slash_command
import members

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="What Can This Bot Do!!", color = discord.Color.nitro_pink())
        embed.add_field(name="`/createsession`", value="Creates a tutoring session with a member")
        embed.add_field(name="`/leaderboard`",value="Get the leaderboard of people for various categories")
        embed.add_field(name="`/userinfo`",value="Gives you info about the user")
        embed.add_field(name="`/rps`", value = "Play a game of rock paper scissors with another person")
        embed.add_field(name="`/gift`", value = "Gift some of your EdCoins 🪙 to another user.")
        embed.add_field(name="`/bug`", value = "Report a bug!")
        embed.add_field(name="`/hocuspocus`", value="What's this 👀")
        embed.set_footer(text="i was developed by Achintya#4448",icon_url=self.client.user.display_avatar)
        await ctx.send(embed = embed)
    @slash_command(name="help", description="Gives you a list of the commands available for the bot")
    async def help1(self, ctx):
        embed = discord.Embed(title="What Can This Bot Do!!", color = discord.Color.nitro_pink())
        embed.add_field(name="`/createsession`", value="Creates a tutoring session with a member")
        embed.add_field(name="`/leaderboard`",value="Get the leaderboard of people for various categories")
        embed.add_field(name="`/userinfo`",value="Gives you info about the user")
        embed.add_field(name="`/rps`", value = "Play a game of rock paper scissors with another person")
        embed.add_field(name="`/gift`", value = "Gift some of your EdCoins 🪙 to another user.")
        embed.add_field(name="`/bug`", value = "Report a bug!")
        embed.add_field(name="`/hocuspocus`", value="What's this 👀")
        embed.set_footer(text="i was developed by Achintya#4448",icon_url=self.client.user.display_avatar)
        await ctx.respond(embed = embed)



def setup(client):
    client.add_cog(Help(client))