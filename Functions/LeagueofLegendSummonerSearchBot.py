#이 코드는 op.gg소환사 전적 검색만을 위한 코드입니다. 추후 다른 기능들을 지속적으로 업데이트 할 예정입니다
#이 코드는 효율성이 많이 떨어지며, 정돈이 아직 덜된상태입니다.
#추후 효율성이 더 높은 코드로 변경할 것이며, selenium을 사용한 버전도 올릴예정입니다

#This code and description is written by Hoplin
#This code is written with API version 1.0.0(Rewirte-V)
#No matter to use it as non-commercial.

# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import discord
import asyncio
import os
from discord.ext import commands
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import youtube_dl
warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='$')
'''
asyncio : Asynchronous I/O. It is a module for asynchronous programming and allows CPU operations to be handled in parallel with I/O.

async def (func name)(parameters): -> This type of asynchronous function or method is called Native Co-Rutine.

- await : you can use await keyword only in Native Co-Rutine

async def add(a,b):
    print("add {0} + {1}".format(a,b))
    await asyncio.sleep(1.0)
    return a + b

async def print_add(a,b):
    result = await add(a,b)
    print("print_add : {0} + {1} = {2}".format(a,b,result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_add(1,2))
loop.close()
'''



def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
    return htmls

bottoken = ''

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("수리중"))
    print("New log in as {0.user}".format(client))


@bot.command()
async def test(ctx,arg):
    await ctx.send(arg)

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith("$lolplayerinfo"):
        playerNickname = ''.join((message.content).split(' ')[1:])
        # Open URL
        checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
        bs = BeautifulSoup(checkURLBool, 'html.parser')

        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0x5CD1E5)
            embed.add_field(name="Summoner name not entered", value="To use command $lolplayerinfo : $lolplayerinfo (Summoner Nickname)", inline=False)
            await message.channel.send("Error : Incorrect command usage ",embed=embed)

        elif len(deleteTags(bs.findAll('h2',{'class' : 'Title'}))) != 0:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.",value="소환사 이름을 체크해주세요", inline=False)
            await message.channel.send("Error : Non existing Summoner ", embed=embed)
        else:
            try:
                #Scrape Summoner's Rank information
                # [Solorank,Solorank Tier]
                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                solorank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                #[Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div',{'class':{'sub-tier__rank-type','sub-tier__rank-tier','sub-tier__league-point', 'sub-tier__gray-text'}}))
                #['Flextier W/L]
                flexrank_Point_and_winratio = deleteTags(bs.findAll('span',{'class' : {'sub-tier__gray-text'}}))

                #솔랭, 자랭 둘다 배치 안되어있는 경우
                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,inline=False)
                    embed.add_field(name="Rank Not Found", value="Unranked",inline=False)
                    embed.set_image(url='https://opgg-static.akamaized.net/images/logo/2015/reverse.rectangle.png')
                    await message.channel.send("소환사 " + playerNickname + "의 전적", embed=embed)

                #솔로랭크 기록이 없는경우
                elif len(solorank_Point_and_winratio) == 0:
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.set_image(url='https://opgg-static.akamaized.net/images/logo/2015/reverse.rectangle.png')
                    await message.channel.send("소환사 " + playerNickname + "의 전적", embed=embed)

                #자유랭크 기록이 없는경우
                elif len(flexrank_Point_and_winratio) == 0:
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.set_image(url='https://opgg-static.akamaized.net/images/logo/2015/reverse.rectangle.png')
                    await message.channel.send("소환사 " + playerNickname + "의 전적", embed=embed)
                else:
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.set_image(url='https://opgg-static.akamaized.net/images/logo/2015/reverse.rectangle.png')
                    await message.channel.send("소환사 " + playerNickname + "의 전적", embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x5CD1E5)
                embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                await message.channel.send("Wrong Summoner Nickname")

            except UnicodeEncodeError as e:
                embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x5CD1E5)
                embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                await message.channel.send("Wrong Summoner Nickname", embed=embed)

client.run(bottoken)
