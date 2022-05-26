from discord.ext import commands
import discord
import myBot
from discord.commands import Option,slash_command
import members

class Award(commands.Cog):
  def __init__(self,client) -> None:
      self.client=client
  @slash_command(name="award",description = "Award points to a tutor")
  @commands.has_any_role(883840894418182165,843466315125227550,941949149291626536,941949149291626536)
  async def award(self,ctx,member:Option(discord.Member,"Tutor to award points",required=True),points:Option(int,"Points to award",required=True)):
    await ctx.defer()

    if member == ctx.author:
      await ctx.reply(embed=discord.Embed(title="I don't think you're supposed to do that.",color=discord.Color.purple()))
      return

    if points <= 0 :
      await ctx.reply(embed=discord.Embed(title=":face_with_raised_eyebrow:",color=discord.Color.purple()))
      return

    members.addPoints(member.id, member, points)
    members.increaseCommandsUsed(ctx)

    
    await ctx.reply(embed=discord.Embed(title=f"Successfully awarded {points} points to {member}",color=discord.Color.green()))
      
      
def setup(client):
 client.add_cog(Award(client))