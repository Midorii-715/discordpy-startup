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
intents=discord.Intents.all()
intents.typing = False  # typingを受け取らないように
client = discord.Client(intents=intents)

member_id_nurro = 702524538692304896
member_id_gamer = 569491014914408450
member_id_sengoku = 569167714137014273
member_id_syachiku = 706855638642458687
member_id_suginokoha = 698837644821528606
member_id_midorii = 281764400942022657
member_midorii = client.get_user(member_id_midorii)

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
        await message.channel.send(f"{member_midorii.mention} へのメンション")
    elif ('妖夢'in message.content) or ('youmu' in message.content):
        member = client.get_user(member_id_midorii)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} 妖夢ちゃん")
    elif ('狂' in message.content) or ('大魔神' in message.content) or ('サクレ' in message.content)or ('ビーフジャーキー' in message.content):
        member = client.get_user(member_id_nurro)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} 狂人")
    elif ('スターリン' in message.content) or ('ヨシフ' in message.content) or ('Stalin' in message.content)or ('Ста́лин' in message.content) :
        member = client.get_user(member_id_suginokoha)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} 粛清")
    elif ('ソ連' in message.content) or ('ソビエト連邦' in message.content)  :
        member = client.get_user(member_id_suginokoha)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} https://youtu.be/xSr5ewJvVig")
        
            
    
    

    
    
    
    
#bot.run(token)
client.run(token)
