from discord.ext import commands
from discord.commands import Option,slash_command

urls = {
  "Tutoring": "https://myeduvisa.org/get-involved/tutoring",
  "Mentorship" : "https://myeduvisa.org/get-involved/mentorship",
  "Others" : "https://myeduvisa.org/get-involved/specializations"
}
 

class Involve(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name = "getinvolved", description = "Join our team!")
    async def getinvolved(self, ctx, team:Option(str, "What team would you like to join?", required=True, choices=['Tutoring', 'Mentorship', 'Outreach', 'Curriculum', 'Human Resources', 'Marketing', 'Engagement', 'Technology'])):
        if team=="Tutoring":
            button1 = discord.ui.Button(
                label="Tutoring", url=urls["Tutoring"]
            )
        elif team=="Mentorship":
            button1 = discord.ui.Button(
                label="Mentorship", url=urls["Mentorship"]
            )
        else:
            button1 = discord.ui.Button(
                label=f"{team}", url=urls["Others"]
            )
        view = discord.ui.View(button1)
        return await ctx.respond(embed=discord.Embed(title=f"Fill in the following form to join the {team} team.",color=discord.Color.nitro_pink()),view=view)

def setup(client):
    client.add_cog(Involve(client))
