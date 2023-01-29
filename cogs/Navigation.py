from discord.ext import commands
from discord.commands import slash_command

server_id = "707278018405466253"
urls = {
  "Directory": "https://discord.com/channels/" + server_id + "/" + "817367374042628146",
  "Rules" : "https://discord.com/channels/" + server_id + "/" + "745203509183643649",
  "Announcements" : "https://discord.com/channels/" + server_id + "/" + "707282430222008441",
  "About Us" : "https://discord.com/channels/" + server_id + "/" + "707282490813055138",
  "FAQs" : "https://discord.com/channels/" + server_id + "/" + "817376694851207178",
  "Suggestions" : "https://discord.com/channels/" + server_id + "/" + "800029963843010590",
  "Social Posts" : "https://discord.com/channels/" + server_id + "/" + "844289506308128768",
  "Partners" : "https://discord.com/channels/" + server_id + "/" + "728654429686857768",
  "SAT" : "https://discord.com/channels/" + server_id + "/" + "745187253986394153",
  "ACT" : "https://discord.com/channels/" + server_id + "/" + "745187327634047036",
  "Bump Our Server" : "https://discord.com/channels/" + server_id + "/" + "765600086825893909",
  "Promotions" : "https://discord.com/channels/" + server_id + "/" + "717254796486377472",
  "Event Stage" : "https://discord.com/channels/" + server_id + "/" + "989359448176885790",
  "Resources" : "https://discord.com/channels/" + server_id + "/" + "707320245827665920",
  "Community Library" : "https://discord.com/channels/" + server_id + "/" + "991119585090744390",
}
 

class Navigation(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @slash_command(name = "navigation", description = "Navigate to our important discord channels!")
    async def navigation(self, ctx):
        button1 = discord.ui.Button(
            label="Directory", url=urls["Directory"])
        button2 = discord.ui.Button(
            label="Rules", url=urls["Rules"])
        button3 = discord.ui.Button(
            label="Announcements", url=urls["Announcements"])
        button4 = discord.ui.Button(
            label="About Us", url=urls["About Us"])
        button5 = discord.ui.Button(
            label="FAQs", url=urls["FAQs"])
        button6 = discord.ui.Button(
            label="Suggestions", url=urls["Suggestions"])
        button7 = discord.ui.Button(
            label="Social Posts", url=urls["Social Posts"])
        button8 = discord.ui.Button(
            label="Partners", url=urls["Partners"])
        button9 = discord.ui.Button(
            label="SAT", url=urls["SAT"])
        button10 = discord.ui.Button(
            label="ACT", url=urls["ACT"])
        button11 = discord.ui.Button(
            label="Bump Our Server", url=urls["Bump Our Server"])
        button12 = discord.ui.Button(
            label="Promotions", url=urls["Promotions"])
        button13 = discord.ui.Button(
            label="Event Stage", url=urls["Event Stage"])
        button14 = discord.ui.Button(
            label="Resources", url=urls["Resources"])
        button15 = discord.ui.Button(
            label="Community Library", url=urls["Community Library"])
        view = discord.ui.View(button1,button2,button3,button4,button5,button6,button7,button8,button9,button10,button14,button15,button11,button12,button13)
        return await ctx.respond(embed=discord.Embed(title="All links for important channels in the server can be found below!",color=discord.Color.nitro_pink()),view=view)

def setup(client):
    client.add_cog(Navigation(client))
