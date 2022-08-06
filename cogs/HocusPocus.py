from discord.ext import commands
from discord.commands import slash_command
import members


class Hocuspocus(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name = "hocuspocus", description = "What's this 👀?")
    async def hocuspocus(self, ctx):
        await ctx.respond("https://imgur.com/NQinKJB")
        await ctx.send(content="||P.S. If you're angry, go rage on <@388347046328926212> because he was the one who suggested this ✌️ (these pings will annoy him as well :D)||",)
        members.increaseCommandsUsed(ctx)




def setup(client):
    client.add_cog(Hocuspocus(client))
