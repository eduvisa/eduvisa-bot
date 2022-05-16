import aiosqlite
import asyncio


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


asyncio.run(setup_db())
