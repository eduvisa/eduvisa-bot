from discord.ext import commands
import discord
import myBot
from discord.commands import Option, slash_command
import members
import random
randomFooters = ["yay", "😎", "wow so cool",
                 "great job!"]
class Deposit(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name="deposit", description="Deposit some of your coins from your wallet to your bank")
    async def deposit(self, ctx, amount: Option(str, "Amount of coins to deposit, max for all", required=True)):
        await ctx.defer()
        walletBalance = members.getValue(
            "walletBalance", ctx.author.id, ctx.author, False)

        if amount == "max" or amount == "all":
            amount = walletBalance
        else:
            try:
                amount = int(amount)
            except Exception:
                return await ctx.respond(embed=discord.Embed(title="Invalid Value", description=f"**'{amount}'** is not a valid value", color=discord.Color.red()))

        if amount > walletBalance:
            return await ctx.respond(embed=discord.Embed(title="Not Enough Money", description=f"You currently do not have **{amount} EdCoins 🪙** in your wallet!\n\nWallet Balance: **{walletBalance} EdCoins 🪙**", color=discord.Color.red()))

        members.updateValue(ctx.author.id, ctx.author, "walletBalance",
                            f"walletBalance-{amount}")
        members.updateValue(ctx.author.id, ctx.author, "bankBalance",
                            f"bankBalance+{amount}")
        bankBalance = members.getValue(
            "bankBalance", ctx.author.id, ctx.author, False)
        embed = discord.Embed(
            title=f"Successfully deposited {amount} EdCoins 🪙!", color=discord.Color.green())
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name="Current Wallet Balance",
                        value=f"**{walletBalance-amount} EdCoins 🪙**", inline=False)
        embed.add_field(name="Current Bank Balance",
                        value=f"**{bankBalance} EdCoins 🪙**", inline=False)
        embed.set_footer(text=f"{random.choice(randomFooters)}")
        await ctx.respond(embed=embed)
    
    @slash_command(name="withdraw", description="Withdraw some of your coins from your bank to your wallet")
    async def withdraw(self, ctx, amount: Option(str, "Amount of coins to withdraw, max for all", required=True)):
        await ctx.defer()
        bankBalance = members.getValue(
            "bankBalance", ctx.author.id, ctx.author, False)

        if amount == "max" or amount == "all":
            amount = bankBalance
        else:
            try:
                amount = int(amount)
            except Exception:
                return await ctx.respond(embed=discord.Embed(title="Invalid Value", description=f"**'{amount}'** is not a valid value", color=discord.Color.red()))

        if amount > bankBalance:
            return await ctx.respond(embed=discord.Embed(title="Not Enough Money", description=f"You currently do not have **{amount} EdCoins 🪙** in your bank!\n\nBank Balance: **{bankBalance} EdCoins 🪙**", color=discord.Color.red()))

        members.updateValue(ctx.author.id, ctx.author, "walletBalance",
                            f"walletBalance+{amount}")
        members.updateValue(ctx.author.id, ctx.author, "bankBalance",
                            f"bankBalance-{amount}")
        walletBalance = members.getValue(
            "walletBalance", ctx.author.id, ctx.author, False)
        embed = discord.Embed(
            title=f"Successfully deposited {amount} EdCoins 🪙!", color=discord.Color.green())
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name="Current Bank Balance",
                        value=f"**{bankBalance-amount} EdCoins 🪙**", inline=False)
        embed.add_field(name="Current Wallet Balance",
                        value=f"**{walletBalance} EdCoins 🪙**", inline=False)
        embed.set_footer(text=f"{random.choice(randomFooters)}")
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Deposit(client))