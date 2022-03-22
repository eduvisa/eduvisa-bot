from discord.ext import commands
import discord
from datetime import date, datetime,timezone
import myBot
from discord.commands import Option,slash_command
import youtube_dl
import pafy
import asyncio
from bs4 import BeautifulSoup
import requests
import aiohttp
    
currentSong = None





client=myBot.client
def getSongTitle(url):
  reqs = requests.get(url)
  soup = BeautifulSoup(reqs.text, 'html.parser')
  songName = ""
  for title in soup.find_all('title'):
    songName= title.get_text()

  
  return songName.replace(" - YouTube","")

class Player(commands.Cog):
  def __init__(self,client) -> None:
      self.client=client
      self.song_queue = []
  

  async def search_songs(self,amount, song, get_url=False):
    info = (await self.client.loop.run_in_executor(None, lambda :youtube_dl.YoutubeDL({"format":"bestaudio","quiet":True}))).extract_info(f"ytsearch{amount}:{song}",download = False,ie_key="YoutubeSearch") 
    if len(info["entries"]) == 0: return None
    
    return [entry["webpage_url"] for entry in info["entries"]] if get_url else info
  async def check_queue(self,ctx):
    global currentSong
    if len(self.song_queue) >0:
      abc=self.song_queue[0]
      await self.play_song(ctx,abc[0])
      await ctx.send(embed=discord.Embed(description=f"**NOW PLAYING**: *{abc[1]}*\n\n**Song was added by**: {abc[2].mention}",color=discord.Color.dark_red()))
      currentSong = self.song_queue[0]
      self.song_queue.pop(0)
    else:
      currentSong=None
      print(currentSong)
  async def play_song(self,ctx,song):
    url = pafy.new(song).getbestaudio().url
    ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)),after=lambda error: self.client.loop.create_task(self.check_queue(ctx)))
    ctx.voice_client.source.volume= 0.5


  @commands.command(name="join")
  async def join(self,ctx):
    if ctx.author.voice is None:
      return await ctx.send(embed=discord.Embed(title="Please connect to a voice channel first :(",color=discord.Color.red()))
    
    if ctx.voice_client is not None:
      await ctx.voice_client.disconnect()
    
    await ctx.author.voice.channel.connect()
  @commands.command(name="leave")
  async def leave(self,ctx):
    if ctx.voice_client is not None:
      self.song_queue.clear()
      embed=discord.Embed(title="Leaving the voice chat!",color=discord.Color.green())
      embed.set_footer(text="Clearing the current song queue")
      await ctx.send(embed=embed)
      
      return await ctx.voice_client.disconnect()
    
    await ctx.send(embed=discord.Embed(title="The bot is currently not in a voice channel"))
  
  @commands.command(name="play",aliases=["p"])
  async def play(self,ctx:commands.Context,*,song=None):
    global currentSong
    if song==None:
      return await ctx.send(embed=discord.Embed(title="Please specify the song",color=discord.Color.red()))
    if ctx.voice_client is None:
      if ctx.author.voice is None:
        return await ctx.send(embed=discord.Embed(title="Please connect to a voice channel first :(",color=discord.Color.red()))
      await ctx.author.voice.channel.connect()
      await ctx.send(embed=discord.Embed(title=f"Successfully joined the voice channel",color=discord.Color.green()))

    if not("youtube.com/watch/" in song or "https://youtu.be" in song):
      message = await ctx.send(embed=discord.Embed(title="Searching for the song, this may take a few seconds... ",color=discord.Color.green()))
      result = await self.search_songs(1,song,get_url=True)
      if result[0] is None:
        return await ctx.send(embed=discord.Embed(title="❌ Could not find the song...",color=discord.Color.red()))
      song=result[0]
    if ctx.voice_client.source is not None:
      
      queue_len = len(self.song_queue)
      if currentSong == None :
        ctx.voice_client.stop()
        await self.play_song(ctx,song)
        currentSong=song
        await message.edit(embed=discord.Embed(title=f"Successfully found the song",description=f"\n\n**NOW PLAYING :  {getSongTitle(song)}**",color=discord.Color.green()))
        print("There is not a song playing")
        print(currentSong)
        return
      elif currentSong!= None:
        print("There is a song playing")
        print(currentSong)
        self.song_queue.append([song,getSongTitle(song),ctx.author])
        
        embed=discord.Embed(title=f"Successfully added the song!",description=f"\n\n Song : **{getSongTitle(song)}** \n\n Queue Position : **{queue_len+1}**",color=discord.Color.green())
        return await message.edit(embed=embed)
    await self.play_song(ctx,song)

    currentSong=song
    await message.edit(embed=discord.Embed(title=f"Successfully found the song",description=f"\n\n**NOW PLAYING :  {getSongTitle(song)}**",color=discord.Color.green()))

  @commands.command()
  async def search(self, ctx,entries:int=5, *, song=None):
      try:entries=int(entries)
      except:entries=5
      if song is None: return await ctx.reply("You forgot to include a song to search for.")

      message = await ctx.send("Searching for song, this may take a few seconds.")

      info = await self.search_songs(entries, song)

      embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.dark_red())
      
      amount = 0
      for entry in info["entries"]:
          embed.description += f"**{amount+1}.**\t{entry['title']}({entry['webpage_url']})\n\n"
          amount += 1

      embed.set_footer(text=f"Displaying the first {amount} results.")
      await message.edit(embed=embed)
  @commands.command()
  async def queue(self, ctx,remove=None,index=None): # display the current guilds queue
    
    if remove =="r" or remove=="remove" and index==None:
      return await ctx.send(embed=discord.Embed(title="Please specify the song to remove from the queue",color=discord.Color.red()))
    elif remove=="r" or remove=="remove" and index != None:
      try:
        indexToRemove=int(index)-1
      except:
        return await ctx.send(embed=discord.Embed(title="Please specify the index of song to clear",color=discord.Color.red()))
      try:
        abc = self.song_queue[indexToRemove]
      except Exception:
        return await ctx.send(embed=discord.Embed(title=f"No song exists at index: {index}",color=discord.Color.red()))
      
      if abc[2] == ctx.author:
        embed=discord.Embed(title="Successfuly Removed the Song",description=f"Removed the Song : **{abc[1]}**\n\n Current Queue Length : **{len(self.song_queue)-1}**",color=discord.Color.green())
        self.song_queue.remove(abc)
        await ctx.send(embed=embed)
        return
      elif abc[2]!= ctx.author:
        embed=discord.Embed(title="Not Your Song",description = f"This song was added by {abc[2].mention} \n\n **YOU CAN NOT REMOVE IT**\n\n **If {abc[2].mention} reacts to the emoji, the song will be skipped**",color=discord.Color.dark_red())
        embed.set_footer(text="they have 15 seconds to respond")
        message=await ctx.send(embed=embed)
        message_id=message.id

        await message.add_reaction("⏩")
        await asyncio.sleep(15)

        message=await ctx.channel.fetch_message(message_id)

        for reaction in message.reactions:
          if reaction=="⏩":
            async for user in reaction.users():
              if user == abc[2]:
                embed=discord.Embed(title="Successfuly Removed the Song",description=f"Removed the Song : **{abc[1]}**\n\n Current Queue Length : **{len(self.song_queue)-1}**",color=discord.Color.green())
                self.song_queue.remove(abc)
                await message.edit(embed=embed)
                return
    elif remove!="remove" or remove!= "r":
      pass
    if len(self.song_queue) == 0:
        return await ctx.send("There are currently no songs in the queue.")
    elif len(self.song_queue) > 0:
      
      embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_red())
      i = 1
      for song in self.song_queue:
          embed.description += f"{i}) **{song[1]}**\n"
          i += 1

      await ctx.send(embed=embed)
  @commands.command()
  async def skip(self,ctx):
    if ctx.voice_client is None:
      return await ctx.send(embed=discord.Embed(title="I am not playing any song!",color=discord.Color.red()))
    if ctx.author.voice is None:
      return await ctx.send(embed=discord.Embed(title="You are not in a voice channel",color=discord.Color.red()))
    if ctx.author.voice.channel.id !=ctx.voice_client.channel.id:
      return await ctx.send(embed=discord.Embed(title="Not playing any songs for you right now.",color=discord.Color.red()))
    
    poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**55% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.dark_red())
    poll.add_field(name="Skip", value=":white_check_mark:")
    poll.add_field(name="Stay", value=":no_entry_sign:")
    poll.set_footer(text="Voting ends in 15 seconds.")

    poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
    poll_id = poll_msg.id

    await poll_msg.add_reaction(u"\u2705") # yes
    await poll_msg.add_reaction(u"\U0001F6AB") # no
    
    await asyncio.sleep(15) # 15 seconds to vote

    poll_msg = await ctx.channel.fetch_message(poll_id)

    votes = {u"\u2705": 0, u"\U0001F6AB": 0}
    reacted = []


    for reaction in poll_msg.reactions:
      if reaction.emoji in [u"\u2705",u"\U0001F6AB"]:
        async for user in reaction.users():
          if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
            votes[reaction.emoji] +=1
            reacted.append(user.id)
    skip=False

    if votes[u"\u2705"] > 0:
      if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.54: # 50% or higher
          skip = True
          embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.green())
    if not skip:
      embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 55% of the members to skip.**", colour=discord.Colour.red())
    embed.set_footer(text="Voting has ended.")
    await poll_msg.clear_reactions()
    await poll_msg.edit(embed=embed)

    if skip:
      ctx.voice_client.stop()
  @commands.command(name="forceskip",aliases=['fs'])
  async def forceskip(self,ctx):
    if ctx.voice_client is None:
      return await ctx.send(embed=discord.Embed(title="I am not playing any song!",color=discord.Color.red()))
    if ctx.author.voice is None:
      return await ctx.send(embed=discord.Embed(title="You are not in a voice channel",color=discord.Color.red()))
    if ctx.author.voice.channel.id !=ctx.voice_client.channel.id:
      return await ctx.send(embed=discord.Embed(title="Not playing any songs for you right now.",color=discord.Color.red()))
    ctx.voice_client.stop()
  @commands.command()
  async def pause(self, ctx):
      if ctx.voice_client.is_paused():
          return await ctx.send("I am already paused.")

      ctx.voice_client.pause()
      await ctx.send("The current song has been paused.")

  @commands.command()
  async def resume(self, ctx):
      if ctx.voice_client is None:
          return await ctx.send("I am not connected to a voice channel.")

      if not ctx.voice_client.is_paused():
          return await ctx.send("I am already playing a song.")
      
      ctx.voice_client.resume()
      await ctx.send("The current song has been resumed.")
  @commands.command()
  async def lyrics(self, ctx, *, song):
 
          url = "https://some-random-api.ml/lyrics"
          song = song.replace(" ", "+")
          data = {
              "title" : song
          }
  
          async with aiohttp.ClientSession() as session:
                  async with session.get(url, data=data) as resp:
                      r = await resp.json()
          if 'error' in r:
              return await ctx.send(r['error'])
          
          em = discord.Embed(
              title=r['title'],
              description=f"{r['lyrics']}", color=discord.Color.random()
          )
          em.set_author(name=r['author'])
          em.set_thumbnail(url=r['thumbnail']['genius'])
          em.color = ctx.author.color
  
          await ctx.send(embed=em)

def setup(client):
  client.add_cog(Player(client))
