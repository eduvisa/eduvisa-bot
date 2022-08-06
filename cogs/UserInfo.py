from discord.ext import commands
import discord
from discord.commands import Option,slash_command
import members
import time

class Userinfo(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name="userinfo",description="Tells information about a member")
    async def userinfo(self, ctx, member:Option(discord.Member, "Member to get information about", required=True)):
        await ctx.defer()
        if members.getValue("isTutor",member.id, member, False) == 1:
            tutoringData = members.getValue("volunteerMinutes",member.id, member, False)
            
            data = members.getValue("netWorth, points, commandsUsed",member.id, member, True)
            netWorth = data[0]
            points = data[1]
            commandsUsed = data[2]
            embed = discord.Embed(
                title=f"{member}", description="**----------TUTORING INFORMATION----------**", color=member.color)
            embed.add_field(
                name="Volunteer Hours", value=f"{int(tutoringData/60)} hours {tutoringData%60} minutes \n -----------------------------------", inline=False)
            embed.add_field(
                name="Date Joined", value=f"<t:{int(time.mktime(member.joined_at.timetuple()))}>")
            embed.add_field(name="Highest Role",
                            value=f"{member.top_role.mention}", inline=False)
            embed.add_field(name="Account Created",
                            value=f"<t:{int(time.mktime(member.created_at.timetuple()))}>\n-----------------------------------", inline=False)
            embed.add_field(name="Commands Used", value=str(commandsUsed))
            embed.add_field(name="Points", value=str(points), inline=False)
            embed.add_field(name="Net Worth", value=f"{netWorth} EdCoins 🪙", inline=False)
            embed.set_thumbnail(url=member.display_avatar)
            members.increaseCommandsUsed(ctx)
            await ctx.respond(embed=embed)
        else:
            data = members.getValue(
                "netWorth, points, commandsUsed", member.id, member, True)
            netWorth = data[0]
            points = data[1]
            commandsUsed = data[2]
            embed = discord.Embed(title=f"{member}", color=member.color)
            embed.add_field(
                name="Date Joined", value=f"<t:{int(time.mktime(member.joined_at.timetuple()))}>")
            embed.add_field(name="Highest Role",
                            value=f"{member.top_role.mention}", inline=False)
            embed.add_field(name="Account Created",
                            value=f"<t:{int(time.mktime(member.created_at.timetuple()))}>\n-----------------------------------", inline=False)
            embed.add_field(name="Commands Used", value=str(commandsUsed))
            embed.add_field(name="Points", value=str(points), inline=False)
            embed.add_field(name="Net Worth",
                            value=f"{netWorth} EdCoins 🪙", inline=False)
            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url = ctx.author.display_avatar)
            members.increaseCommandsUsed(ctx)
            await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Userinfo(client))