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
intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

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
    # 「おはよう」で始まるか調べる
    if message.content.startswith("おはよう"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            m = "おはようございます" + message.author.name + "さん！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await message.channel.send(m)
     # 「/neko」と発言したら「にゃーん」が返る処理
    elif message.content == '/neko':
        await message.channel.send('にゃーん')
    elif message.content.startswith('/word '):
        count = -5
        for i in range(len(message.content)):
            m = message.content
            c = m[i]
            if ((c != " ") and (c != "-")and (c != "'")and (c != "　")):
                count += 1
        await message.channel.send(count)
    elif message.content == '/Midorii':
        member_id = 281764400942022657
        member = client.get_user(member_id)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} へのメンション")
            
    
    

    
    
    
    
#bot.run(token)
client.run(token)
