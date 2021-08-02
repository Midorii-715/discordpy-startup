from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(token)


import discord
from discord.ext import commands

bot = commands.Bot(
    command_prefix="!"
)

presence = discord.Game("Qiita") # Qiitaをプレイ中

@bot.event
async def on_ready():
    await bot.change_presence(activity=presence)
