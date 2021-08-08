from discord.ext import commands
import sys
#import tweepy
import getteteets
import os
import traceback
#test
import discord
import asyncio
import random

import os

# 迷路用
# from .maze import Maze

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

# 迷路用
# maze = Maze()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await asyncio.sleep(10)
    #twitterからのツイートを取得
    tweetsListener = MyStreamListener()
    tweetsListener.on_status()



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
    elif message.content.startswith('/roll'):
        if('d' in message.content):
            digit_dice = 0
            digit_roll  = 0
            flg_num_dice = 0
            str_result = ""
            num_dice = []
            num_roll = []
            for i in range(len(message.content)):
                m = message.content
                c = m[i]
            
                if ((c == "0") or (c == "1") or (c == "2") or (c == "3") or (c == "4") or (c == "5") or (c == "6") or (c == "7") or (c == "8") or (c == "9")):
                    if(flg_num_dice ==0):
                        num_dice[digit_dice] = int(c) 
                        digit_dice += 1
                    elif(flg_num_dice ==1):
                        num_roll[digit_roll] = int(c)
                        digit_roll += 1
                elif(c == "d"):
                    flg_num_dice = 1
            for j in range(digit_dice):
                dice += num_dice[j] * 10**(digit_dice-j-1)
            if(flg_num_dice == 0):
                roll = 1
            elif(flg_num_dice == 1):
                for j in range(digit_roll):
                    roll += num_roll[j] * 10**(digit_roll-j-1)
            sum_res = 0
            for k in range(roll):
                result = random.randint(1, dice)
                sum_res += result
                if (k == roll-1):
                    str_result += str(result)
                else:
                    str_result += str(result) + "+"
                
                
        str_message = f"{message.author.mention}" + str_result + "=" + str(res)
        await message.channel.send(str_message) 
    elif message.content == '/money': 
        i = random.randint(0, 9999)
        j = random.randint(0, 3)
        str_unit =""
        get_money = i
        if j == 0:
            str_unit = ""
        elif j == 1:
            str_unit = "万"
            get_money *= 10**4
        elif j == 2:
            str_unit = "億"
            get_money *= 10**8
        elif j == 3:
            str_unit = "兆"
            get_money *= 10**12
        elif j == 4:
            str_unit = "京"
        str_money = str(i) + str_unit
        str_message = f"{message.author.mention}" + str_money + "円GET!"
        await message.channel.send(str_message)
        
    elif message.content == '/Midorii':
        member_midorii = client.get_user(member_id_midorii)
        await message.channel.send(f"{member_midorii.mention} へのメンション")
    elif ('狂' in message.content) or ('大魔神' in message.content) or ('サクレ' in message.content)or ('ビーフジャーキー' in message.content):
        member = client.get_user(member_id_nurro)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} 狂人")
    elif ('スターリン' in message.content) or ('ヨシフ' in message.content) or ('Stalin' in message.content)or ('Ста́лин' in message.content) :
        member = client.get_user(member_id_suginokoha)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} 粛清")
    elif ('音割れ' in message.content) :
        member = message.author
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} https://youtu.be/vrmcVVftseI")
    elif ('うんこ' in message.content) or ('unko' in message.content):
        j = random.randint(1, 3)
        member = message.author
        #member = message.channel.guild.get_member(member_id)
        if (j == 3):
            await message.channel.send(f"{member.mention} うんこ💩")
        else:
            await message.channel.send(f"{member.mention} 草")
    elif ('うんち' in message.content) or ('unchi' in message.content):
        j = random.randint(1, 3)
        member = message.author
        #member = message.channel.guild.get_member(member_id)
        if (j == 3):
            await message.channel.send(f"{member.mention} うんち！w")
        else:
            await message.channel.send(f"{member.mention} 草")
    elif ('ソ連' in message.content) or ('ソビエト連邦' in message.content) or ('蘇維埃社会主義共和国連邦' in message.content)or ('蘇維埃' in message.content)or ('ソビエト社会主義共和国連邦' in message.content)or ('ソビエトロシア' in message.content)or ('ソビエト' in message.content) :
        member = client.get_user(member_id_suginokoha)
        #member = message.channel.guild.get_member(member_id)
        await message.channel.send(f"{member.mention} https://youtu.be/xSr5ewJvVig")

    # 迷路の処理
    # maze.process(message)

@client.event
async def tweet(ctx):
    await ctx.send('nyan')
    
#bot.run(token)
client.run(token)
