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
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room



###################################################################
#Parse Operator's icon from ubisoft.com
operatoriconURLDict = dict()
# Scrape Rainbow Six Siege's Operator's icon before start
unisoftURL = "https://www.ubisoft.com"
rainbowSixSiegeOperatorIconURL = "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators"
html = requests.get(rainbowSixSiegeOperatorIconURL).text
bs = BeautifulSoup(html,'html.parser')

#Get oprators' pages with ccid
operatorListDiv = bs.findAll('div',{'ccid' : re.compile('[0-9A-Za-z]*')})
print(len(operatorListDiv))
for ind in range(0,len(operatorListDiv)):
    print(ind + 1)
    operatormainURL = operatorListDiv[ind].a['href']
    #Get Operator's name
    operatorname = operatormainURL.split('/')[-1]
    #Open URL : each operator's pages
    html2 = requests.get(unisoftURL + operatormainURL).text
    bs2 = BeautifulSoup(html2, 'html.parser')
    print(operatorname)
    operatoriconURL = bs2.find('div',{'class' : "operator__header__icons__names"}).img['src']
    operatoriconURLDict[operatorname] = operatoriconURL
###################################################################

# for lolplayersearch
tierScore = {
    'default' : 0,
    'iron' : 1,
    'bronze' : 2,
    'silver' : 3,
    'gold' : 4,
    'platinum' : 5,
    'diamond' : 6,
    'master' : 7,
    'grandmaster' : 8,
    'challenger' : 9
}
def tierCompare(solorank,flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2

# for Rainbow Six Siege
#r6stats 서버에서 크롤링을 막은듯하다
r6URL = "https://r6stats.com"
playerSite = 'https://www.r6stats.com/search/'

warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='!')

opggsummonersearch = 'https://www.op.gg/summoner/userName='

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
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type !help or !도움말 for help"))
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

    if message.content.startswith("!help") or message.content.startswith("!도움말"):
        embed = discord.Embed(title="Stats Search bot commands", description="", color=0x5CD1E5)
        embed.add_field(name="Rainbow Six Siege stat search", value="!레식전적 (닉네임)",inline=False)
        embed.add_field(name="Rainbow Six Siege Stats by Operator", value="!레식오퍼 (닉네임)",inline=False)
        embed.add_field(name="League of Legend stat search", value="!롤전적 (닉네임)", inline=False)
        embed.add_field(name="Covid-19 Virus Korea status", value="!코로나", inline=False)
        embed.add_field(name="Source Code", value="!sourcecode",inline=False)
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Command List", embed=embed)

    if message.content.startswith("!sourcecode"):
        embed = discord.Embed(title="Stats Search bot's sourcdcodes.", description="All of the codes are written in Python3",color=0x5CD1E5)
        embed.add_field(name="Rainbow Six Siege search", value="Github : https://github.com/J-hoplin1/Rainbow-Six-Siege-Search-bot/blob/master/RainbowSixSIegeSearchBot.py", inline=False)
        embed.add_field(name="Rainbow Six Siege search by operators",
                        value="Github : https://github.com/J-hoplin1/Rainbow-Six-Siege-Search-bot/blob/master/RainbowSixSIegeSearchBot.py", inline=False)
        embed.add_field(name="League of Legend search",value="Github : https://github.com/J-hoplin1/League-Of-Legend-Search-Bot",inline=False)
        embed.add_field(name="Covid-19 Virus Korea status",value="Github : https://github.com/J-hoplin1/Covid19-Information-bot/blob/master/Covid19KoreaStatusBot.py", inline=False)
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Search bot's souce code is open source!", embed=embed)

    if message.content.startswith("!롤전적"):
        playerNickname = ''.join((message.content).split(' ')[1:])
        # Open URL
        checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
        bs = BeautifulSoup(checkURLBool, 'html.parser')

        # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다
        RankMedal = bs.findAll('img', {
            'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
        # index 0 : Solo Rank
        # index 1 : Flexible 5v5 rank

        # for mostUsedChampion
        mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
        mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

        # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0x5CD1E5)
            embed.add_field(name="Summoner name not entered",
                            value="To use command $lolplayerinfo : $lolplayerinfo (Summoner Nickname)", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Incorrect command usage ", embed=embed)

        elif len(deleteTags(bs.findAll('h2', {'class': 'Title'}))) != 0:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Non existing Summoner ", embed=embed)
        else:
            try:
                # Scrape Summoner's Rank information
                # [Solorank,Solorank Tier]
                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))
                # ['Flextier W/L]
                flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                # embed.set_imag()는 하나만 들어갈수 있다.

                # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)

                # 솔로랭크 기록이 없는경우
                elif len(solorank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)

                # 자유랭크 기록이 없는경우
                elif len(flexrank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + "WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
                # 두가지 유형의 랭크 모두 완료된사람
                else:
                    # 더 높은 티어를 thumbnail에 안착
                    solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                    # Make State
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    if cmpTier == 0:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])

                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x5CD1E5)
                embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                await message.channel.send("Wrong Summoner Nickname")

            except UnicodeEncodeError as e:
                embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x5CD1E5)
                embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                await message.channel.send("Wrong Summoner Nickname", embed=embed)

    if message.content.startswith("!레식전적"):


        #Get player nickname and parse page
        playerNickname = ''.join((message.content).split(' ')[1:])
        html = requests.get(playerSite + playerNickname + '/pc/').text
        print(playerSite + playerNickname + '/pc/')
        bs = BeautifulSoup(html, 'html.parser')

        #한번에 검색 안되는 경우에는 해당 반환 리스트의 길이 존재. -> bs.find('div',{'class' : 'results'}

        if bs.find('div',{'class' : 'results'}) == None:
            # Get latest season's Rank information
            latestSeason = bs.find('div', {'class': re.compile('season\-rank operation\_[A-Za-z_]*')})

            # if player nickname not entered
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="플레이어 이름이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Player name not entered" + playerNickname,
                                value="To use command : !레식전적 (nickname)")
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Player name not entered ", embed=embed)

            # search if it's empty page
            elif latestSeason == None:
                embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Can't find player name " + playerNickname,
                                value="Please check player's nickname")
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Can't find player name " + playerNickname, embed=embed)

            # Command entered well
            else:

                # r6stats profile image
                r6Profile = bs.find('div', {'class': 'main-logo'}).img['src']

                # player level
                playerLevel = bs.find('span', {'class': 'quick-info__value'}).text.strip()

                RankStats = bs.find('div', {'class': 'card stat-card block__ranked horizontal'}).findAll('span', {
                    'class': 'stat-count'})
                # Get text from <span> values
                for info in range(len(RankStats)):
                    RankStats[info] = RankStats[info].text.strip()
                # value of variable RankStats : [Timeplayed, Match Played,kills per matchm, kills,death, KDA Rate,Wins,Losses,W/L Rate]

                # latest season tier medal
                lastestSeasonRankMedalLocation = latestSeason.div.img['src']
                # latest Season tier
                lastestSeasonRankTier = latestSeason.div.img['alt']
                # latest season operation name
                OperationName = latestSeason.find('div', {'class': 'meta-wrapper'}).find('div', {
                    'class': 'operation-title'}).text.strip()
                # latest season Ranking
                latestSeasonRanking = latestSeason.find('div', {'class': 'rankings-wrapper'}).find('span',
                                                                                                   {'class': 'ranking'})

                # if player not ranked, span has class not ranked if ranked span get class ranking
                if latestSeasonRanking == None:
                    latestSeasonRanking = bs.find('span', {'class': 'not-ranked'}).text.upper()
                else:
                    latestSeasonRanking = latestSeasonRanking.text

                embed = discord.Embed(title="Rainbow Six Siege player search from r6stats", description="",
                                      color=0x5CD1E5)
                embed.add_field(name="Player search from r6stats", value=playerSite + playerNickname + '/pc/',
                                inline=False)
                embed.add_field(name="Operation : " + OperationName,
                                value="Tier : " + lastestSeasonRankTier + " / " + "Ranking : #" + latestSeasonRanking + " / " + "Level : " + playerLevel,
                                inline=False)

                embed.add_field(name="Total Play Time", value=RankStats[0], inline=True)
                embed.add_field(name="Match Played", value=RankStats[1], inline=True)
                embed.add_field(name="Kills per match", value=RankStats[2], inline=True)
                embed.add_field(name="Total Kills", value=RankStats[3], inline=True)
                embed.add_field(name="Total Deaths", value=RankStats[4], inline=True)
                embed.add_field(name="K/D Ratio", value=RankStats[5], inline=True)
                embed.add_field(name="Wins", value=RankStats[6], inline=True)
                embed.add_field(name="Losses", value=RankStats[7], inline=True)
                embed.add_field(name="W/L Ratio", value=RankStats[8], inline=True)
                embed.set_thumbnail(url=r6URL + r6Profile)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Player " + playerNickname + "'s stats search", embed=embed)
        else:
            searchLink = bs.find('a',{'class' : 'result'})
            if searchLink == None:
                embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Can't find player name " + playerNickname,
                                value="Please check player's nickname")
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Can't find player name " + playerNickname, embed=embed)
            else:
                searchLink = r6URL + searchLink['href']
                html = requests.get(searchLink).text
                bs = BeautifulSoup(html,'html.parser')
                # Get latest season's Rank information
                latestSeason = bs.find('div', {'class': re.compile('season\-rank operation\_[A-Za-z_]*')})

                # if player nickname not entered
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="플레이어 이름이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Error : Player name not entered" + playerNickname,
                                    value="To use command : !레식전적 (nickname)")
                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Error : Player name not entered ", embed=embed)

                # search if it's empty page
                elif latestSeason == None:
                    embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                    embed.add_field(name="Error : Can't find player name " + playerNickname,
                                    value="Please check player's nickname")
                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Error : Can't find player name " + playerNickname, embed=embed)

                # Command entered well
                else:

                    # r6stats profile image
                    r6Profile = bs.find('div', {'class': 'main-logo'}).img['src']

                    # player level
                    playerLevel = bs.find('span', {'class': 'quick-info__value'}).text.strip()

                    RankStats = bs.find('div', {'class': 'card stat-card block__ranked horizontal'}).findAll('span', {
                        'class': 'stat-count'})
                    # Get text from <span> values
                    for info in range(len(RankStats)):
                        RankStats[info] = RankStats[info].text.strip()
                    # value of variable RankStats : [Timeplayed, Match Played,kills per matchm, kills,death, KDA Rate,Wins,Losses,W/L Rate]

                    # latest season tier medal
                    lastestSeasonRankMedalLocation = latestSeason.div.img['src']
                    # latest Season tier
                    lastestSeasonRankTier = latestSeason.div.img['alt']
                    # latest season operation name
                    OperationName = latestSeason.find('div', {'class': 'meta-wrapper'}).find('div', {
                        'class': 'operation-title'}).text.strip()
                    # latest season Ranking
                    latestSeasonRanking = latestSeason.find('div', {'class': 'rankings-wrapper'}).find('span', {
                        'class': 'ranking'})

                    # if player not ranked, span has class not ranked if ranked span get class ranking
                    if latestSeasonRanking == None:
                        latestSeasonRanking = bs.find('span', {'class': 'not-ranked'}).text.upper()
                    else:
                        latestSeasonRanking = latestSeasonRanking.text

                    embed = discord.Embed(title="Rainbow Six Siege player search from r6stats", description="",
                                          color=0x5CD1E5)
                    embed.add_field(name="Player search from r6stats", value=playerSite + playerNickname + '/pc/',
                                    inline=False)
                    embed.add_field(name="Operation : " + OperationName,
                                    value="Tier : " + lastestSeasonRankTier + " / " + "Ranking : #" + latestSeasonRanking + " / " + "Level : " + playerLevel,
                                    inline=False)

                    embed.add_field(name="Total Play Time", value=RankStats[0], inline=True)
                    embed.add_field(name="Match Played", value=RankStats[1], inline=True)
                    embed.add_field(name="Kills per match", value=RankStats[2], inline=True)
                    embed.add_field(name="Total Kills", value=RankStats[3], inline=True)
                    embed.add_field(name="Total Deaths", value=RankStats[4], inline=True)
                    embed.add_field(name="K/D Ratio", value=RankStats[5], inline=True)
                    embed.add_field(name="Wins", value=RankStats[6], inline=True)
                    embed.add_field(name="Losses", value=RankStats[7], inline=True)
                    embed.add_field(name="W/L Ratio", value=RankStats[8], inline=True)
                    embed.set_thumbnail(url=r6URL + r6Profile)
                    embed.set_footer(text='Service provided by Hoplin.',
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Player " + playerNickname + "'s stats search", embed=embed)




    if message.content.startswith("!레식오퍼"):
        #operator image dictionary key is lowercase

        #for player's operator Informaiton
        useroperatorInformation = dict()

        playerNickname = ''.join((message.content).split(' ')[1:])
        html = requests.get(playerSite + playerNickname + '/pc/').text
        bs = BeautifulSoup(html, 'html.parser')

        if bs.find('div',{'class' : 'results'}) == None:
            # Scrape menu hyperlink : to operator menu
            playerOperator = bs.find('a', {'class': 'player-tabs__operators'})
            playerOperatorMenu = r6URL + playerOperator['href']
            print(playerOperatorMenu)
            # Reopen page
            html = requests.get(playerOperatorMenu).text
            bs = BeautifulSoup(html, 'html.parser')

            embed = discord.Embed(title="Stats by operator", description="Arrange in order of high-play operator",
                                  color=0x5CD1E5)

            operatorStats = bs.findAll('tr', {'class': 'operator'})

            mostOperator = None

            indNumS = 0
            # statlist -> [operator,kills,deaths,K/D,Wins,Losses,W/L,HeadShots,Melee Kills,DBNO,Playtime]
            for op in operatorStats:
                # discord can show maximum 8 fields
                if indNumS == 7:
                    break
                count = 0
                statlist = []
                if op.td.span.text.split(" ")[-1] == "Recruit":
                    pass
                else:
                    for b in op:
                        statlist.append(b.text)
                    if indNumS == 0:
                        mostOperator = statlist[0].lower()
                    embed.add_field(name="Operator Name", value=statlist[0], inline=True)
                    embed.add_field(name="Kills / Deaths", value=statlist[1] + "K / " + statlist[2] + "D", inline=True)
                    embed.add_field(name="Wins / Losses", value=statlist[4] + "W / " + statlist[5] + "L", inline=True)
                    indNumS += 1
            embed.set_thumbnail(url=operatoriconURLDict[mostOperator])
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Player " + playerNickname + "'s stats search", embed=embed)
        else:
            searchLink = bs.find('a', {'class': 'result'})
            if searchLink == None:
                embed = discord.Embed(title="해당 이름을 가진 플레이어가 존재하지않습니다.", description="", color=0x5CD1E5)
                embed.add_field(name="Error : Can't find player name " + playerNickname,
                                value="Please check player's nickname")
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Can't find player name " + playerNickname, embed=embed)
            else:
                searchLink = bs.find('a',{'class' : 'result'})['href']
                searchLink = r6URL + searchLink
                html = requests.get(searchLink).text
                bs = BeautifulSoup(html,'html.parser')
                # Scrape menu hyperlink : to operator menu
                playerOperator = bs.find('a', {'class': 'player-tabs__operators'})
                playerOperatorMenu = r6URL + playerOperator['href']
                print(playerOperatorMenu)
                # Reopen page
                html = requests.get(playerOperatorMenu).text
                bs = BeautifulSoup(html, 'html.parser')

                embed = discord.Embed(title="Stats by operator", description="Arrange in order of high-play operator",
                                      color=0x5CD1E5)

                operatorStats = bs.findAll('tr', {'class': 'operator'})

                mostOperator = None

                indNumS = 0
                # statlist -> [operator,kills,deaths,K/D,Wins,Losses,W/L,HeadShots,Melee Kills,DBNO,Playtime]
                for op in operatorStats:
                    # discord can show maximum 8 fields
                    if indNumS == 7:
                        break
                    count = 0
                    statlist = []
                    if op.td.span.text.split(" ")[-1] == "Recruit":
                        pass
                    else:
                        for b in op:
                            statlist.append(b.text)
                        if indNumS == 0:
                            mostOperator = statlist[0].lower()
                            if mostOperator == "jäger":
                                mostOperator = 'jager'
                            else:
                                pass
                        embed.add_field(name="Operator Name", value=statlist[0], inline=True)
                        embed.add_field(name="Kills / Deaths", value=statlist[1] + "K / " + statlist[2] + "D",
                                        inline=True)
                        embed.add_field(name="Wins / Losses", value=statlist[4] + "W / " + statlist[5] + "L",
                                        inline=True)
                        indNumS += 1
                embed.set_thumbnail(url=operatoriconURLDict[mostOperator])
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Player " + playerNickname + "'s stats search", embed=embed)

    if message.content.startswith("!코로나"):
        # 보건복지부 코로나 바이러스 정보사이트"
        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})
        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = totalPeopletoInt[0] + totalPeopletoInt[1]
        lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
        embed = discord.Embed(title="Covid-19 Virus Korea Status", description="", color=0x5CD1E5)
        embed.add_field(name="Data source : Ministry of Health and Welfare of Korea",
                        value="http://ncov.mohw.go.kr/index.jsp", inline=False)
        embed.add_field(name="Latest data refred time",
                        value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 " + latestupdateTime[
                            2] + " 자료입니다.", inline=False)
        embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1] + "(" + beforeNum[0] + ")", inline=True)
        embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        embed.add_field(name="누적확진률", value=statNum[6], inline=True)
        embed.add_field(name="치사율", value=str(lethatRate) + " %", inline=True)
        embed.set_thumbnail(
            url="https://ww.namu.la/s/90fc57e8957024083e7745a8d46ade60e98b7d9b244b5c7d033b815c77eac0930af09691fe4a03953c8425c45ce5335ce340bf20634092f1ed191c52e269794070f3e4febe4412eb8277352b72de00f8d210a279531f0229fb8e5ec77dddcf31413b8a4eaddf8d1624e15a8907e3ae32")
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Covid-19 Virus Korea Status", embed=embed)
client.run(bottoken)
