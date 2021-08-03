from discord.ext import commands
import os
import traceback
#test
import discord
import asyncio
import random
import sys
import os

#test
# bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await asyncio.sleep(10)



@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@client.event
async def ping(ctx):
    await ctx.send('pong')
    
@client.event
async def neko(ctx):
    await ctx.send('nyan')
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
       
@client.event
async def on_message(message):
    # 「おはよう」で始まるか調べる
    if message.content.startswith("おはよう"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            m = "おはようございます" + message.author.name + "さん！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await message.channel.send(m)
    
    
@client.event
async def words(ctx):
    await ctx.send('nyan')
    s = input("word")

    count = 0
    for i in range(len(s)):
        c = s[i]
        if ((c != " ") and (c != "-")and (c != "'")):
            count += 1
    print(count)
    await ctx.send(count)
    
    
    
    
bot.run(token)
