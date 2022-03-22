from discord.ext import commands
import discord
import myBot
from discord.commands import Option,slash_command
import members


class Invite(commands.Cog):
  def __init__(self,client):
    self.client=client

  @slash_command(name="invite",description="Get the invite link ir invite a user to the server")
  async def invite1(self,ctx):

    inviteLink = await ctx.channel.create_invite()
    await ctx.respond(f"Here's the permanent invite link to Eduvisa : \n\n{inviteLink}")
    members.increaseCommandsUsed(ctx)




def setup(client):
  client.add_cog(Invite(client))
    
    
    