from discord.ext import commands
import discord
import members
from discord.commands import Option, slash_command
import members
from discord.ui import button as button
import random
winningPairs = [["Rock","Scissors"],["Paper","Rock"],["Scissors","Paper"]]

emojis = {
    "Rock" : "👊",
    "Paper" : "🖐️",
    "Scissors" : "✌️"
}


async def validateResult(userChoice, interaction, botChoice, author, ctx,bet=None):
    pair = [userChoice, botChoice]
    if pair in winningPairs:
        embed = discord.Embed(title="You won the game",
                         color=discord.Color.green())
        embed.add_field(name="Bot's Choice", value=f"{emojis[botChoice]}", inline=True)
        embed.add_field(name="Your Choice", value=f"{emojis[userChoice]}", inline=True)
        if bet!=None:
            embed.add_field(name="Winning Amount",value=f"You won the bet so I have credited **{bet} EdCoins 🪙** to your wallet!", inline=False)
            members.updateValue(author.id, author,
                                "walletBalance", f"walletBalance+{bet}")
        embed.set_footer(text="very cool.")
        
        await interaction.response.edit_message(embed=embed, view=None)
    elif userChoice==botChoice:
        embed = discord.Embed(title="You drew the game",
                              color=discord.Color.dark_grey())
        embed.add_field(name="Bot's Choice",
                        value=f"{emojis[botChoice]}", inline=True)
        embed.add_field(name="Your Choice",
                        value=f"{emojis[userChoice]}", inline=True)
        if bet!=None:
            embed.add_field(
                name="Winning Amount", value=f"Nothing has changed in your wallet :p", inline=False)
        embed.set_footer(text="cool.")
        await interaction.response.edit_message(embed=embed, view=None)
    else:
        embed = discord.Embed(title="You lost the game",
                              color=discord.Color.red())
        embed.add_field(name="Bot's Choice",
                        value=f"{emojis[botChoice]}", inline=True)
        embed.add_field(name="Your Choice",
                        value=f"{emojis[userChoice]}", inline=True)
        if bet!=None:
            embed.add_field(
                name="Losing Amount", value=f"You lost the bet so I have debited **{bet} EdCoins 🪙** from your wallet", inline=False)
            members.updateValue(ctx.author.id, ctx.author, "walletBalance", f"walletBalance-{bet}")
        embed.set_footer(text="not cool.")
        await interaction.response.edit_message(embed=embed, view=None)

    members.increaseCommandsUsed(ctx)

class NoMemberRPS(discord.ui.View):
 def __init__(self, ctx, client, bet):
     super().__init__(timeout=35)
     self.randChoice = random.choice(["Rock", "Paper", "Scissors"])
     self.ctx = ctx
     self.client = client
     self.bet = bet

 @discord.ui.button(emoji="👊", style=discord.ButtonStyle.primary)
 async def button_callback(self, button, interaction):
   await validateResult("Rock",interaction,self.randChoice,self.ctx.author, self.ctx, bet=self.bet)

 @discord.ui.button(emoji="🖐", style=discord.ButtonStyle.primary)
 async def button_callback1(self, button, interaction):
     await validateResult("Paper", interaction, self.randChoice,
                    self.ctx.author, self.ctx, bet=self.bet)

 @discord.ui.button(emoji="✌", style=discord.ButtonStyle.primary)
 async def button_callback2(self, button, interaction):
     await validateResult("Scissors", interaction, self.randChoice,
                    self.ctx.author, self.ctx, bet=self.bet)

 async def interaction_check(self, interaction: discord.Interaction) -> bool:
    if interaction.user != self.ctx.author:
        await interaction.response.send_message("yeah good luck playing someone else's game", ephemeral=True)
        return False
    else:
        return True

class MemberConsent(discord.ui.View):
    def __init__(self, member, author, ctx):
        self.member = member
        self.author = author
        self.ctx = ctx
        super().__init__(timeout=30)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.member:
            await interaction.response.send_message("yeah i don't think you're supposed to do that?", ephemeral=True)
            return False
        else:
            return True
    @button(label="👍 Alright!", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        button.disabled = True
    
    @button(label="❌ NO!", style=discord.ButtonStyle.red)
    async def button_callback1(self, button, interaction):
        for items in self.children : items.disabled = True
        ##print("Pressed NO!")
        await interaction.response.edit_message(view=self)
        return await interaction.followup.send("too bad", view=None)

class RPS(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name="rps", description="Play a game of rock-paper-scissors with the bot or another member and bet money!")
    async def rps(self, ctx,member:Option(discord.Member,"Member to play rock paper scissors with", default=None), bet:Option(str,"Your bet against the bot", required = False, default=None)):
            await ctx.defer()
            if member == None:
                if bet!=None:
                    cash = members.getValue(
                        "walletBalance", ctx.author.id, ctx.author, False)

                    if bet.lower() == "max" or bet.lower() == "all":
                        bet = cash
                    else:
                        try:
                            bet = int(bet)
                            if cash < bet:
                                return await ctx.respond(embed=discord.Embed(title="Not enough money", description=f"You currently do not have **{bet} EdCoins 🪙** in your wallet!", color=discord.Color.red()))

                        except:
                            return await ctx.send(embed=discord.Embed(title = "Invalid Value", description = f"**'{bet}'** is not a valid value", color = discord.Color.red()))

                view = NoMemberRPS(ctx,self.client,bet)
                await ctx.respond(embed=discord.Embed(title="Pick rock, paper or scissors!",color=discord.Color.purple()),view=view)
        
            else:
                await ctx.respond(embed=discord.Embed(title="alr here you go", color=discord.Color.green()), view=MemberConsent(member, ctx.author, ctx))






def setup(client):
    client.add_cog(RPS(client))