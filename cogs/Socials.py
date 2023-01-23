from discord.ext import commands
import discord
from discord.commands import Option,slash_command

#dictionary including all the links
urls = {
  "instagram" : "https://www.instagram.com/myeduvisa/",
  "linkedin" : "https://www.linkedin.com/company/myeduvisa/",
  "reddit" : "https://www.reddit.com/user/eduvisa/",
  "facebook" :"https://www.facebook.com/teameduvisa/",
  "twitter" : "https://twitter.com/myeduvisa",
  "website" : "https://www.myeduvisa.org",
  "dc" : "https://discord.gg/RcffyjxUP9",
  "youtube" : "https://www.youtube.com/channel/UC6KGOBlBVm8yp172XAoNKdQ"
}

class Socials(commands.Cog):
    def __init__(self,client):
        self.client=client

    @slash_command(name="socials",description="Get the EduVisa social media for a specific platform or all of them")
    async def socials(self, ctx, platform: Option(str, "Platform to get socials for", required=False, default="All", choices=["Instagram", "LinkedIn", "Reddit", "Facebook", "YouTube", "Twitter", "Website", "Discord", "All"])):
        global button1 
    
        if platform=="All":
            button1 = discord.ui.Button(
                  label="Instagram", url=urls["instagram"])
            button2 = discord.ui.Button(
                  label="LinkedIn", url=urls["linkedin"])
            button3 = discord.ui.Button(
                  label="Reddit", url=urls["reddit"])
            button4 = discord.ui.Button(
                  label="Facebook", url=urls["facebook"])
            button5 = discord.ui.Button(
                  label="YouTube", url=urls["youtube"])
            button6 = discord.ui.Button(
                  label="Twitter", url=urls["twitter"])
            button7 = discord.ui.Button(
                  label="Website", url=urls["website"])
            button8 = discord.ui.Button(
                  label="Discord", url=urls["dc"])
            view = discord.ui.View(button1,button2,button3,button4,button5,button6,button7,button8)

            return await ctx.respond(embed=discord.Embed(title="All links for socials can be found below!",color=discord.Color.nitro_pink()),view=view)

        platformc = platform.lower()
        if platformc == "discord": platformc="dc"
    
        button1 = discord.ui.Button(label=f"{platform}", url=urls[platformc])
        view=discord.ui.View(button1)

        return await ctx.respond(embed=discord.Embed(title=f"Here's our {platform}",color=discord.Color.nitro_pink()),view=view)
    



def setup(client):
  client.add_cog(Socials(client))
  