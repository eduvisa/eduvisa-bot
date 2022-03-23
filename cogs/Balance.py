from calendar import c
from discord.ext import commands
import discord
from datetime import date, datetime, timezone
import myBot
from discord.commands import Option, slash_command
import members

class Balance(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @slash_command(name="balance", description="View your EdCoins🪙 balance or another member's")
    async def balance(self, ctx, member:Option(discord.Member, "Member to get the balance for", required=False)):
        if member==None:
            member = ctx.author
        balance = members.getValue("walletBalance, bankBalance",member.id, member, fetchmany=True)
        bb = balance[1]
        wb = balance[0]

        embed = discord.Embed(
            title=f"{member.name}'s Balance", description=f"Wallet: **{balance[0]} 🪙**\nBank: **{balance[1]} 🪙**", color=discord.Color.dark_red())
        members.increaseCommandsUsed(ctx)
        return await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Balance(client))