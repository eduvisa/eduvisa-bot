from discord.ext import commands
import discord
import members
from discord.commands import Option, slash_command
import members
from discord.ui import button as button
import random
winningPairs = [["Rock","Scissors"],["Paper","Rock"],["Scissors","Paper"]]
randomFooters = ["yay", "😎", "wow so cool",
                 "great job!", "meh", "yo thats sick!!"]

emojis = {
    "Rock" : "👊",
    "Paper" : "🖐️",
    "Scissors" : "✌️"
}


async def validateResult(userChoice, interaction, botChoice, author, ctx, view, bet=None):
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
async def validateResultWithMembers(userChoice, memberChoice, member, interaction, ctx, bet=None):
    pair = [userChoice, memberChoice]
    global embed
    if pair in winningPairs:
        embed = discord.Embed(title=f"{ctx.author} won the game!",
                              color=discord.Color.nitro_pink())
        embed.add_field(name=f"{member.name}'s Choice",
                        value=f"{emojis[memberChoice]}", inline=True)
        embed.add_field(name=f"{ctx.author.name}'s Choice",
                        value=f"{emojis[userChoice]}", inline=True)
        
        if bet != None:
            embed.add_field(
                name="Winning Amount", value=f"{ctx.author.mention} won the bet so I have credited **{bet} EdCoins 🪙** to their wallet!\n\nAlso, {member.mention} loses that much amount 😔", inline=False)
            members.updateValue(ctx.author.id, ctx.author,
                                "walletBalance", f"walletBalance+{bet}")
            members.updateValue(member.id, member, "walletBalance", f"walletBalance-{bet}")
        
        embed.set_footer(text=f"{random.choice(randomFooters)}")

    elif userChoice == memberChoice:
        embed = discord.Embed(title=f"DRAW!",
                              color=discord.Color.nitro_pink())
        embed.add_field(name=f"{member.name}'s Choice",
                        value=f"{emojis[memberChoice]}", inline=True)
        embed.add_field(name=f"{ctx.author.name}'s Choice",
                        value=f"{emojis[userChoice]}", inline=True)

        if bet != None:
            embed.add_field(
                name="Winning Amount", value=f"No changes happened to the balance", inline=False)

        embed.set_footer(text=f"{random.choice(randomFooters)}")
    else:
        embed = discord.Embed(title=f"{member} won the game",
                              color=discord.Color.nitro_pink())
        embed.add_field(name=f"{member.name}'s Choice",
                        value=f"{emojis[memberChoice]}", inline=True)
        embed.add_field(name=f"{ctx.author.name}'s Choice",
                        value=f"{emojis[userChoice]}", inline=True)

        if bet != None:
            embed.add_field(
                name="Winning Amount", value=f"{member.mention} won the bet so I have credited **{bet} EdCoins 🪙** to their wallet!\n\nAlso, {ctx.author.mention} loses that much amount 😔", inline=False)
            members.updateValue(ctx.author.id, ctx.author,
                                "walletBalance", f"walletBalance-{bet}")
            members.updateValue(member.id, member,
                                "walletBalance", f"walletBalance+{bet}")

        embed.set_footer(text=f"{random.choice(randomFooters)}")
    members.increaseCommandsUsed(ctx)
    members.updateValue(member.id, member, "commandsUsed", "commandsUsed + 1")
    await interaction.followup.send(content=f"{member.mention}\n{ctx.author.mention}", embed=embed, view=None)

    

class NoMemberRPS(discord.ui.View):
 def __init__(self, ctx, client, bet, message):
     super().__init__(timeout=30)
     self.randChoice = random.choice(["Rock", "Paper", "Scissors"])
     self.ctx = ctx
     self.client = client
     self.bet = bet
     self.message = message
     self.isDone = False

 @discord.ui.button(emoji="👊", style=discord.ButtonStyle.primary)
 async def button_callback(self, button, interaction):
   await validateResult("Rock", interaction, self.randChoice, self.ctx.author, self.ctx, self, bet=self.bet)
   self.isDone = True

 @discord.ui.button(emoji="🖐", style=discord.ButtonStyle.primary)
 async def button_callback1(self, button, interaction):
     await validateResult("Paper", interaction, self.randChoice,
                    self.ctx.author, self.ctx, self , bet=self.bet)
     self.isDone = True

 @discord.ui.button(emoji="✌", style=discord.ButtonStyle.primary)
 async def button_callback2(self, button, interaction):
     await validateResult("Scissors", interaction, self.randChoice,
                          self.ctx.author, self.ctx, self, bet=self.bet)
     self.isDone = True
 async def interaction_check(self, interaction: discord.Interaction) -> bool:
    if interaction.user != self.ctx.author:
        await interaction.response.send_message("yeah good luck playing someone else's game", ephemeral=True)
        return False
    else:
        return True

 async def on_timeout(self) -> None:
    for child in self.children:
         child.disabled = True
    await self.ctx.edit(view = self)
    if not self.isDone:
        await self.ctx.respond("oops")
    return






class MemberConsent(discord.ui.View):
    def __init__(self, member, author, ctx, bet):
        self.member = member
        self.author = author
        self.ctx = ctx
        self.bet = bet
        self.isDone = False
        super().__init__(timeout=30)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.member:
            await interaction.response.send_message("yeah i don't think you're supposed to do that?", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.ctx.edit(view=self)
        if not self.isDone:
            await self.ctx.respond("well thats sad :(")
        return
    @button(label="👍 Alright!", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        chance = random.choice([self.member, self.author])
        view = PersonRPS(self.member, self.ctx, self.bet)
        embed = discord.Embed(title="Rock Paper Scisssors", description="Please pick your choices", color = discord.Color.nitro_pink())
        embed.set_footer(text="You have 30 seconds to respond!")
        self.timeout = 0
        self.isDone = True
        await interaction.response.edit_message(content=f"{self.author.mention}\n{self.member.mention}",embed=embed, view = view)
        button.disabled = True
    
    @button(label="❌ NO!", style=discord.ButtonStyle.red)
    async def button_callback1(self, button, interaction):
        for items in self.children : items.disabled = True
        await interaction.response.edit_message(view=self)
        self.timeout = 0
        self.isDone = True
        return await interaction.followup.send("too bad", view=None)

class PersonRPS(discord.ui.View):
    def __init__(self, member, ctx, bet):
        self.member = member
        self.ctx = ctx
        self.isDone = False
        self.playerVotes = {
            member : 0,
            ctx.author : 0
        }
        self.playerChoices = {
            member : None,
            ctx.author : None
        }
        self.bet = bet
        super().__init__(timeout=30)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user not in self.playerVotes.keys():
            await interaction.response.send_message("yeah i don't think you're supposed to do that or you have already responded.... 🤦‍♂️", ephemeral=True)
            return False
        else:
            return True

    async def recordResponses(self,item:str,interaction:discord.Interaction):
        if interaction.user in self.playerVotes.keys():
            if self.playerVotes[interaction.user] > 0:
                await interaction.response.send_message("You have already responded!", ephemeral=True)
            else:
                await interaction.response.send_message("Recorded your response!", ephemeral=True)
                self.playerVotes[interaction.user] = 1
                self.playerChoices[interaction.user] = item

                self.playerVotes.pop(interaction.user)

        if len(self.playerVotes) == 0:
            await validateResultWithMembers(self.playerChoices[self.ctx.author], self.playerChoices[self.member], self.member, interaction, self.ctx, self.bet)

    async def on_timeout(self) -> None:
        global embed
        for child in self.children:
            child.disabled = True
        
        if len(self.playerVotes) != 2:
            
            memberLeft = list(self.playerVotes.keys())[0]
            choicec = self.playerChoices
            choicec.pop(memberLeft)
            if self.bet != None:
                embed = discord.Embed(title=f"{memberLeft} did not respond!", color = discord.Color.purple())
                embed.description = f"Since they have decided to run away, I have credited the bet amount to {list(choicec.keys())[0].mention}\nBet Amount : **{self.bet} EdCoins 🪙**"
                embed.set_footer(text = "P.S. Don't want the amount? Give them the amount back by using /gift")
                members.updateValue(list(choicec.keys())[
                                    0].id, list(choicec.keys())[0], "commandsUsed", "commandsUsed + 1")
            else:
                embed = discord.Embed(
                    title=f"{memberLeft} did not respond!", color=discord.Color.purple())
                embed.description = f"They just straight up **took-off**"
                members.updateValue(list(choicec.keys())[
                                    0].id, list(choicec.keys())[0], "commandsUsed", "commandsUsed + 1")

        elif len(self.playerVotes) == 2:
            embed = discord.Embed(
                title=f"No one wanted to play ig!", color=discord.Color.red())
        else:
            return

        await self.ctx.edit(view=self)
        return await self.ctx.respond(embed=embed)


    @discord.ui.button(label="👊", style=discord.ButtonStyle.primary)
    async def button1(self, button, interaction):
        await PersonRPS.recordResponses(self, "Rock", interaction=interaction)
        
    
    @discord.ui.button(label="🖐️", style=discord.ButtonStyle.primary)
    async def button2(self, button, interaction):
        await PersonRPS.recordResponses(self, "Paper", interaction=interaction)

    @discord.ui.button(label="✌️", style=discord.ButtonStyle.primary)
    async def button3(self, button, interaction):
        await PersonRPS.recordResponses(self, "Scissors", interaction=interaction)







class RPS(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name="rps", description="Play a game of rock-paper-scissors with the bot or another member and bet money!")
    async def rps(self, ctx,member:Option(discord.Member,"User to play rock paper scissors with, the bot is the default", default=None), bet:Option(str,"Your bet against the bot or the user", required = False, default=None)):
            await ctx.defer()
            if member == None or member == self.client.user:
                if bet!=None:
                    cash = members.getValue(
                        "walletBalance", ctx.author.id, ctx.author, False)

                    if bet.lower() == "max" or bet.lower() == "all":
                        bet = cash
                        if bet < 0:
                            return await ctx.send(embed=discord.Embed(title="🤔", color=discord.Color.red()))
                    else:
                        try:
                            bet = int(bet)
                            if cash < bet:
                                return await ctx.respond(embed=discord.Embed(title="Not enough money", description=f"You currently do not have **{bet} EdCoins 🪙** in your wallet!", color=discord.Color.red()))

                        except:
                            return await ctx.send(embed=discord.Embed(title="Invalid Value", description=f"**'{bet}'** is not a valid value", color=discord.Color.red()))
                
                if bet == 0: bet = None
                view = NoMemberRPS(ctx, self.client, bet, None)
                message = await ctx.respond(embed=discord.Embed(title="Pick rock, paper or scissors!", color=discord.Color.purple()), view=view)
                
                
        
            else:
                if member == ctx.author:
                    return await ctx.send(title="How u gonna play a game with yourself?", color = discord.Color.red())
                cash = members.getValue(
                    "walletBalance", ctx.author.id, ctx.author, False)
                memberCash = members.getValue("walletBalance", member.id, member, False)
                if bet!=None:
                    if bet.lower() == "max" or bet.lower() == "all":
                        bet = cash
                    else:
                        try:
                            bet = int(bet)
                            if bet < 0 :
                                return await ctx.send(embed=discord.Embed(title="🤔", color=discord.Color.red()))

                        except:
                            return await ctx.send(embed=discord.Embed(title="Invalid Value", description=f"**'{bet}'** is not a valid value", color=discord.Color.red()))

                    if memberCash < bet:
                        return await ctx.respond(embed=discord.Embed(title="Not enough money", description=f"{member.mention} does not have **{bet} EdCoins 🪙** in their wallet!", color=discord.Color.red()))
                    if cash < bet:
                        return await ctx.respond(embed=discord.Embed(title="Not enough money", description=f"You currently do not have **{bet} EdCoins 🪙** in your wallet!", color=discord.Color.red()))
                    if bet == 0: bet = None
                if bet != None:
                    await ctx.respond(f"{member.mention}", embed=discord.Embed(title=f"Game of RPS with {ctx.author}", description=f"Do you want to bet **{bet} EdCoins 🪙** on a game of rock-paper-scissors with {ctx.author.mention}?", color=discord.Color.nitro_pink()), view=MemberConsent(member, ctx.author, ctx, bet), ephemeral=True)

                else:
                    await ctx.respond(f"{member.mention}", embed=discord.Embed(title=f"Game of RPS with {ctx.author}", description=f"Do you want to play a game of rock-paper-scissors with {ctx.author.mention}?", color=discord.Color.nitro_pink()), view=MemberConsent(member, ctx.author, ctx, None), ephemeral=True)





def setup(client):
    client.add_cog(RPS(client))