import random
from datetime import time, datetime

import discord
from discord.ext import commands, tasks
import aiosqlite



class QuestionsListView(discord.ui.View):
    def __init__(self, ctx, ems):
        super().__init__(timeout=69)
        self.ctx = ctx
        self.em = ems
        self.index = 0

    
    @discord.ui.button(style=discord.ButtonStyle.green, emoji="⬅", custom_id="left")
    async def left(self, button, interaction):
        if self.index == 0:
            button = [x for x in self.children if x.custom_id=="left"][0]
            button.disabled = True
        else:
            button = [x for x in self.children if x.custom_id=="right"][0]
            button.disabled = False
            self.index -= 1
        em = self.em[self.index]
        await interaction.response.edit_message(view=self,embed=em)
    

    @discord.ui.button(style=discord.ButtonStyle.green, emoji="➡️", custom_id="right")
    async def right(self, button, interaction):
        if self.index == (len(self.em)-1):
            button = [x for x in self.children if x.custom_id=="right"][0]
            button.disabled = True
        else:
            button = [x for x in self.children if x.custom_id=="left"][0]
            button.disabled = False
            self.index += 1
        em = self.em[self.index]
        await interaction.response.edit_message(view=self,embed=em)


class QOTD(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.qotd_channel = 815945741096190022
        self.accept_channel = 975420124070838312

        self.qotd_loop.start()

    async def setup_db():
        async with aiosqlite.connect("qotd.db") as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS Questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    question TEXT, 
                    author TEXT, 
                    accepted INTEGER
                )"""
            )
            await db.commit()

    @tasks.loop(time=time(0, 0))
    # @tasks.loop(seconds=10) for debug
    async def qotd_loop(self):
        async with aiosqlite.connect("qotd.db") as db:
            cur = await db.execute("SELECT * FROM Questions WHERE accepted=1")
            data = await cur.fetchall()

            if len(data) == 0:
                return

            question = random.choice(data)

            await db.execute(f"DELETE FROM Questions WHERE id={question[0]}")
            await db.commit()

        channel = await self.client.fetch_channel(self.qotd_channel)

        em = discord.Embed(
            title="QOTD!",
            description=f"Today's question is: \n**{question[1]}**\n",
            color=discord.Color.random()
        )
        em.set_footer(text=f"Question suggested by {question[2]}")
        await channel.send(embed=em)

    @commands.slash_command(name="qotd-suggest", description="Suggest a QOTD")
    async def qotd_suggest(self, ctx, suggestion: str):
        """
        Suggest a qotd to be sent for approval
        """
        channel = self.accept_channel

        em = discord.Embed(
            title="QOTD Suggestion",
            description=suggestion,
            color=ctx.author.color,
            timestamp=datetime.now(),
        )
        em.add_field(name="Suggestor Name:", value=ctx.author.name)

        channel = await self.client.fetch_channel(channel)

        if channel is None:
            return ctx.respond("An error occured while suggesting")

        message = await channel.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        await ctx.respond("Thank you for your suggestion :)")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.client.user.id:
            return
        if payload.channel_id != self.accept_channel:
            return

        channel = await self.client.fetch_channel(self.accept_channel)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        if message.author.id != self.client.user.id:
            return

        try:
            embed = message.embeds[0]
        except AttributeError:
            return
            
        if payload.emoji.name == "❌":
            return await message.delete()

        elif payload.emoji.name == "✅":

            async with aiosqlite.connect("qotd.db") as db:
                await db.execute(
                    """INSERT INTO Questions 
                    (question, author, accepted) VALUES (?, ?, ?)""",
                    (
                        embed.description,
                        embed.fields[0].value,
                        1,
                    ),
                )
                await db.commit()

            content = f"Suggestion approved!\n\nContent: {embed.description}\nAuthor: {embed.fields[0].value}"
            await message.edit(embed=None, content=content)
            await message.clear_reactions()
        else:
            return


    @commands.slash_command(name="list-qotd", description="Lists the qotd questions")
    async def list_qotd_suggestions(self, ctx):
        async with aiosqlite.connect("qotd.db") as db:
            cur = await db.execute("SELECT * FROM Questions WHERE accepted=1")
            data = await cur.fetchall()

            if len(data) == 0:
                return await ctx.respond("No questions")

        embeds_list = []

        counter = 0
        em_counter = 0
        embeds_list.append(discord.Embed(title=f"Page {em_counter+1}", color=discord.Color.random()))
        for id, question, author, accepted in data:
            counter += 1
            if counter >= 10:
                counter = 0
                em_counter += 1

                embeds_list.append(discord.Embed(title=f"Page {em_counter+1}", color=discord.Color.random()))

            embeds_list[em_counter].add_field(name=f"ID: {id} - {author}:", value=question, inline=False)

            
        view = QuestionsListView(ctx,ems=embeds_list)

        await ctx.respond(view=view, content="List of approved question of the day suggestions")


    @commands.slash_command(name="qotd-delete", description="Delete a qotd suggestion")
    async def delete_qotd_command(self, ctx, id:int):

        async with aiosqlite.connect("qotd.db") as db:
            await db.execute(f"DELETE FROM Questions WHERE id=?", (id,))
            await db.commit()

        await ctx.respond("Suggestion deleted!")



def setup(client):
    client.add_cog(QOTD(client))
