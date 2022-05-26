from discord.ext import commands
import discord
import myBot
from discord.commands import Option, slash_command
import members
import random
numberList = []
for i in range(0, 2001):
    numberList.append(i)

for i in range(0,101):
    numberList.insert(0,0)

list = ["be gone",
        "coin.exe has stopped working",
        "go ask someone else",
        "the atm is out of order, sorry",
        "bye jerk, no coins for you",
        "ew no",
        "Back in my day we worked for a living",
        "can you not",
        "I need my money to buy airpods",
        "stop begging",
        "no coins for you",
        "You get nothing",
        "no u",
        "get lost u simp",
        "Imagine begging in 2022, gofundme is where it is at"]

people = ["Rick Astley",
          "Shrek",
          "Jesus",
          "Mr Mosby",
          "Wendy",
          "Barry McKocner",
          "Jordan Peele",
          "Kevin Hart",
          "Drake",
         "Kamala Harris",
          "Chris Peanuts",
          "Rihanna",
          "Mr. Clean",
          "Selena Gomez",
          "Harry",
          "Elizabeth Warren",
         "Dawn Keebals",
          "Billie Eilish",
          "Joe Montana",
          "Chuck Norris",
          "Dr. Phil",
          "Default Jonesy",
          "Cardi B",
          "Peter Dinklage",
          "Nicki Minaj",
          "Dwight Shrute",
          "Timmy",
          "Demi Lovato",
          "Donald Glover",
          "Lady Gaga",
          "Oprah",
          "Elon Musk",
          "Taylor Swift",
          "Justin Bieber",
          "Mike Hoochie",
          "Mike Ock",
          "Jennifer Lopez",
          "Barack Obama",
          "Cersei Lannister",
          "Gordon Ramsay",
          "Emilia Clarke",
          "Keanu Reeves",
          "Mr. Beast"
          ]

class Beg(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @slash_command(name = "beg", description = "Beg for some EdCoins 🪙 from me! I may give them 👀")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx:discord.ApplicationContext):
        global embed
        coins = random.choice(numberList)
        if coins == 0:
            embed = discord.Embed(title = f"{random.choice(people)}", color = discord.Color.red())
            embed.description = f"*\"{random.choice(list)}\"*"
            members.increaseCommandsUsed(ctx)
        else:
            embed = discord.Embed(
                title=f"{random.choice(people)}", color=discord.Color.green())
            embed.description = f"*\"You can have **{coins} EdCoins 🪙**\"*"
            members.updateValue(ctx.author.id, ctx.author, "walletBalance", f"walletBalance + {coins}")
            members.increaseCommandsUsed(ctx)

        await ctx.respond(embed=embed)





    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title = "Easy with the spam!!", color = discord.Color.red())
            embed.description = f"This command is still on cooldown. Please wait **{int(error.retry_after)} seconds**"
            embed.set_footer(text="Default cooldown time is 60 seconds!")
            return await ctx.respond(embed=embed)



def setup(client):
    client.add_cog(Beg(client))