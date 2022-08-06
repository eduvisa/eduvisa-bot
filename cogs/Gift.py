from discord.ext import commands
import discord
from discord.commands import Option, slash_command
import members


class MemberConsent(discord.ui.View):
    def __init__(self, ctx, coins, member):
        self.member = member
        self.author = ctx.author
        self.ctx = ctx
        self.coins = coins
        self.isDone = False
        super().__init__(timeout=30)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
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

    @discord.ui.button(label="👍 Alright!", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        members.updateValue(self.member.id, self.member, "walletBalance", f"walletBalance + {self.coins}")
        members.updateValue(self.ctx.author.id, self.ctx.author,
                            "walletBalance", f"walletBalance - {self.coins}")
        members.increaseCommandsUsed(self.ctx)
        embed = discord.Embed(title = f"{self.ctx.author.name} gifted to {self.member.name}", color = discord.Color.green())
        memberBalance = members.getValue("walletBalance", self.member.id, self.member, False)
        userBalance = members.getValue("walletBalance", self.ctx.author.id, self.ctx.author, False)
        embed.description = f"Successfully gave **{self.coins} EdCoins 🪙** to {self.member.mention}\n\n{self.member.mention}'s Wallet Balance : **{memberBalance} EdCoins 🪙** \n\n Your Wallet Balance : **{userBalance} EdCoins 🪙**"
        embed.set_thumbnail(
            url="https://media3.giphy.com/media/uKi4DG2TPzGuN4Q7Xg/giphy.gif")
        
        for child in self.children:
            child.disabled = True
        self.timeout = 0
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content=f"{self.author.mention}\n{self.member.mention}", embed=embed)
        button.disabled = True
        self.isDone = True

    @discord.ui.button(label="❌ NO!", style=discord.ButtonStyle.red)
    async def button_callback1(self, button, interaction):
        for items in self.children:
            items.disabled = True
        await interaction.response.edit_message(view=self)
        self.timeout = 0
        self.isDone = True
        return await interaction.followup.send("too bad", view=None)




class Gift(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name = "gift", description = "Gift some of your EdCoins 🪙 to a user")
    async def gift(self, ctx, member:Option(discord.Member, "Member to gift coins to", required = True), coins:Option(str, "Coins to gift (max and all are allowed)", required = True)):
        if member == ctx.author or member == self.client.user:
            return await ctx.respond(embed=discord.Embed(title="🤔", color=discord.Color.red()))

        await ctx.defer()
        walletBalance = members.getValue("walletBalance", ctx.author.id, ctx.author, False)

        if coins.lower() == "max" or coins.lower() == "all":
            coins = walletBalance
        else:
            try:
                coins = int(coins)
                if coins <= 0:
                    return await ctx.send(embed=discord.Embed(title="🤔", color=discord.Color.red()))
                if coins > walletBalance:
                    return await ctx.respond(embed=discord.Embed(title="Not enough money", description=f"You currently do not have **{coins} EdCoins 🪙** in your wallet!", color=discord.Color.red()))


            except:
                return await ctx.respond(embed=discord.Embed(title="Invalid Value", description=f"**'{coins}'** is not a valid value", color=discord.Color.red()))


        view = MemberConsent(ctx, coins, member)
        await ctx.respond(embed=discord.Embed(title="Are you sure?", description = f"Are you sure you want to gift **{coins} EdCoins 🪙** to {member.mention}", color=discord.Color.nitro_pink()), view=view)


        



def setup(client):
    client.add_cog(Gift(client=client))