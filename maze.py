import discord
import asyncio




class Maze:
    def __init__(self):
        pass

    async def process(seld, message):
        if message.content == '/maze':
            member =  message.author
            await message.channel.send(f"{member.mention} maze test")

