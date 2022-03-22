from pydoc import describe
from discord.ext import commands
import discord
import members
from discord.commands import Option, slash_command
import members
import random


class MyView(discord.ui.View):
 def __init__(self, ctx, client):
     super().__init__(timeout=35)
     self.randChoice = random.choice(["Rock", "Paper", "Scissors"])
     self.ctx = ctx
     self.client = client

 @discord.ui.button(emoji="👊", style=discord.ButtonStyle.primary)
 async def button_callback(self, button, interaction):
  if self.randChoice == "Rock":
   embed = discord.Embed(title="You drew the game",
                         color=discord.Color.dark_grey())
   embed.add_field(name="Bot's Choice", value="👊", inline=True)
   embed.add_field(name="Your Choice", value="👊", inline=True)
   embed.set_footer(text="cool.", icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  elif self.randChoice == "Paper":
   embed = discord.Embed(title="You lost the game", color=discord.Color.red())
   embed.add_field(name="Bot's Choice", value="🖐", inline=True)
   embed.add_field(name="Your Choice", value="👊", inline=True)
   embed.set_footer(text="not cool.", icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  elif self.randChoice == "Scissors":
   embed = discord.Embed(title="You won the game", color=discord.Color.green())
   embed.add_field(name="Bot's Choice", value="✌", inline=True)
   embed.add_field(name="Your Choice", value="👊", inline=True)
   embed.set_footer(text="very cool.",
                    icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  else:
   await interaction.response.edit_message("**I got an error what the heck**", view=None)

 @discord.ui.button(emoji="🖐", style=discord.ButtonStyle.primary)
 async def button_callback1(self, button, interaction):
  if self.randChoice == "Rock":
   embed = discord.Embed(title="You won the game", color=discord.Color.green())
   embed.add_field(name="Bot's Choice", value="👊", inline=True)
   embed.add_field(name="Your Choice", value="🖐", inline=True)
   embed.set_footer(text="very cool.",
                    icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)

   members.increaseCommandsUsed(self.ctx)
  elif self.randChoice == "Paper":
   embed = discord.Embed(title="You drew the game",
                         color=discord.Color.dark_grey())
   embed.add_field(name="Bot's Choice", value="🖐", inline=True)
   embed.add_field(name="Your Choice", value="🖐", inline=True)
   embed.set_footer(text="cool.", icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  elif self.randChoice == "Scissors":
   embed = discord.Embed(title="You lost the game", color=discord.Color.red())
   embed.add_field(name="Bot's Choice", value="✌", inline=True)
   embed.add_field(name="Your Choice", value="🖐", inline=True)
   embed.set_footer(text="not cool.", icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  else:
   await interaction.response.edit_message("**I got an error what the heck**", view=None)

 @discord.ui.button(emoji="✌", style=discord.ButtonStyle.primary)
 async def button_callback2(self, button, interaction):
  if self.randChoice == "Rock":
   embed = discord.Embed(title="You lost the game", color=discord.Color.red())
   embed.add_field(name="Bot's Choice", value="👊", inline=True)
   embed.add_field(name="Your Choice", value="✌", inline=True)
   embed.set_footer(text="not cool.", icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  elif self.randChoice == "Paper":
   embed = discord.Embed(title="You won the game", color=discord.Color.green())
   embed.add_field(name="Bot's Choice", value="🖐", inline=True)
   embed.add_field(name="Your Choice", value="✌", inline=True)
   embed.set_footer(text="very cool.",
                    icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  elif self.randChoice == "Scissors":
   embed = discord.Embed(title="You drew the game",
                         color=discord.Color.dark_grey())
   embed.add_field(name="Bot's Choice", value="✌", inline=True)
   embed.add_field(name="Your Choice", value="✌", inline=True)
   embed.set_footer(text="cool.", icon_url=self.client.user.display_avatar)
   await interaction.response.edit_message(embed=embed, view=None)
   members.increaseCommandsUsed(self.ctx)
  else:
   await interaction.response.edit_message("**I got an error what the heck**", view=None)

 async def interaction_check(self, interaction: discord.Interaction) -> bool:
    if interaction.user != self.ctx.author:
        await interaction.response.send_message("yeah good luck playing someone else's game", ephemeral=True)
        return False
    else:
        return True
class RPS(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name="rps", description="Play a game of rock-paper-scissors with the bot and bet money!")
    async def rps(self, ctx, bet:Option(int,"Your bet against the bot", required = False, default=None)):
        if bet == None:
            await ctx.defer()
            view = MyView(ctx,self.client)
            await ctx.respond(embed=discord.Embed(title="Pick rock, paper or scissors!",color=discord.Color.purple()),view=view)



def setup(client):
    client.add_cog(RPS(client))