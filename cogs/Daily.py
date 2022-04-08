from discord.ext import commands
import discord
import myBot
from discord.commands import Option, slash_command
import members
import random


class Daily(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @slash_command(name="daily", description="Get some EdCoins 🪙 daily")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def daily(self, ctx):
        await ctx.defer()
        members.cursor.execute(
            f"INSERT OR IGNORE INTO daily(user) VALUES('{ctx.author}');")
        members.db.commit()

        
        members.cursor.execute(
            f"SELECT streak FROM daily WHERE user = '{ctx.author}';")
        [streak] = members.cursor.fetchone()
        members.db.commit()


        embed = discord.Embed(title="Daily Coins successfully collected!", color = discord.Color.nitro_pink())
        embed.description = f"**{25000 + (streak*500)} EdCoins 🪙** were credited to your wallet!\n\n\n"
        
        print("Command is working")
        
        if streak >= 1:
            embed.set_footer(
                text=f"You got {streak*500} extra EdCoins 🪙 because of your {streak} daily streak. | bump us plz 🙏")
        else:
            embed.set_footer(
                text=f"bump us plz 🙏")
        print("got till line 39")
        embed.set_thumbnail(
            url="https://media3.giphy.com/media/uKi4DG2TPzGuN4Q7Xg/giphy.gif")
        print("42")
        members.increaseCommandsUsed(ctx)
        print("44")
        members.updateValue(ctx.author.id, ctx.author, "walletBalance", f"walletBalance + {25000 + (streak*500)}")
        print("46")
        members.cursor.execute(
            f"UPDATE daily SET streak = streak + 1 WHERE user = '{ctx.author}';")
        print("49")
        members.db.commit()
        print("51")
        print("going to be responded")
        await ctx.respond(embed = embed)
        print("already responded lol")


    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Easy with the spam!!", color=discord.Color.red())
            embed.description = f"You have already claimed your daily for today!.\n\n Please wait **{int(int(error.retry_after)/3600)} hours**"
            embed.set_footer(text="😔✌️")
            print("the comman did update")
            return await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Daily(client))
