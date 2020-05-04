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
import unicodedata
import json
from tqdm import tqdm
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
print("Initiating Rainbow Six Siege Operators' Information....")
for ind in tqdm(range(0,len(operatorListDiv))):
    operatormainURL = operatorListDiv[ind].a['href']
    #Get Operator's name
    operatorname = operatormainURL.split('/')[-1]
    #Open URL : each operator's pages
    html2 = requests.get(unisoftURL + operatormainURL).text
    bs2 = BeautifulSoup(html2, 'html.parser')
    operatoriconURL = bs2.find('div',{'class' : "operator__header__icons__names"}).img['src']
    operatoriconURLDict[operatorname] = operatoriconURL
###################################################################

#Naver API Key
client_id = ""
client_secret = ""
bottoken = ''

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

def convertToNormalEnglish(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')

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

    if message.content.startswith("!help") or message.content.startswith("!도움말") or message.content.startswith("!명령어"):
        embed = discord.Embed(title="Stats Search bot commands", description="If there is bug in bot, please contact to me. jhyoon0815103@gmail.com.", color=0x5CD1E5)
        embed.add_field(name="Rainbow Six Siege stat search", value="!레식전적 (닉네임)",inline=False)
        embed.add_field(name="Rainbow Six Siege Stats by Operator", value="!레식오퍼 (닉네임)",inline=False)
        embed.add_field(name="League of Legend stat search", value="!롤전적 (닉네임)", inline=False)
        embed.add_field(name="Covid-19 Virus Korea status", value="!코로나", inline=False)
        embed.add_field(name="MapleStory player information searchbot", value="!메이플 (닉네임)",inline=False)
        embed.add_field(name="PUBG TPP solo player information searchbot", value="!배그솔로1 (닉네임)", inline=False)
        embed.add_field(name="PUBG FPP solo player information searchbot", value="!배그솔로2 (닉네임)", inline=False)
        embed.add_field(name="PUBG TPP duo player information searchbot", value="!배그듀오1 (닉네임)", inline=False)
        embed.add_field(name="PUBG FPP duo player information searchbot", value="!배그듀오2 (닉네임)", inline=False)
        embed.add_field(name="PUBG TPP squad player information searchbot", value="!배그스쿼드1 (닉네임)", inline=False)
        embed.add_field(name="PUBG FPP squad player information searchbot", value="!배그스쿼드2 (닉네임)", inline=False)
        embed.add_field(name="Korean -> English translate",value="!한영번역 (단어 혹은 문장)",inline=False)
        embed.add_field(name="English -> Korean translate", value="!영한번역 (단어 혹은 문장)",inline=False)
        embed.add_field(name="Korean -> Japanese translate", value="!한일번역 (단어 혹은 문장)", inline=False)
        embed.add_field(name="Japanese -> Korean translate", value="!일한번역 (단어 혹은 문장)", inline=False)
        embed.add_field(name="Korean -> Chinese translate", value="!한중번역 (단어 혹은 문장)", inline=False)
        embed.add_field(name="Chinese -> Korean translate", value="!중한번역 (단어 혹은 문장)", inline=False)
        embed.add_field(name="Source Code", value="!sourcecode",inline=False)
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Command List", embed=embed)

    if message.content.startswith("!sourcecode"):
        embed = discord.Embed(title="Stats Search bot's sourcdcodes.", description="All of the codes are written in Python3 and are opensource.\n Do not use these code as commercially",color=0x5CD1E5)
        embed.add_field(name="Rainbow Six Siege search", value="Github : https://github.com/J-hoplin1/Rainbow-Six-Siege-Search-bot/blob/master/RainbowSixSIegeSearchBot.py", inline=False)
        embed.add_field(name="Rainbow Six Siege search by operators",
                        value="Github : https://github.com/J-hoplin1/Rainbow-Six-Siege-Search-bot/blob/master/RainbowSixSIegeSearchBot.py", inline=False)
        embed.add_field(name="League of Legend search",value="Github : https://github.com/J-hoplin1/League-Of-Legend-Search-Bot",inline=False)
        embed.add_field(name="Covid-19 Virus Korea status",value="Github : https://github.com/J-hoplin1/Covid19-Information-bot/blob/master/Covid19KoreaStatusBot.py", inline=False)
        embed.add_field(name="MapleStory player information searchbot",value="Github : https://github.com/J-hoplin1/MapleStory-Character-Information-SearchBot/blob/master/MapleStoryBot.py",inline=False)
        embed.add_field(name="PUBG player information searchbot",value="Github : https://github.com/J-hoplin1/PUBG-player-search-bot/blob/master/PUBGSearchbot.py",inline=False)
        embed.add_field(name="Papago translate bot",value="Github : https://github.com/J-hoplin1/Papago-API-Bot/blob/master/PapagoBot.py",inline=False)
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Search bot's souce code is open source!", embed=embed)

    if message.content.startswith("!롤전적"):
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0x5CD1E5)
                embed.add_field(name="Summoner name not entered",
                                value="To use command !롤전적 : !롤전적 (Summoner Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)
            else:
                playerNickname = ''.join((message.content).split(' ')[1:])
                # Open URL
                checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
                bs = BeautifulSoup(checkURLBool, 'html.parser')

                # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다

                # Patch Note 20200503에서
                # Medal = bs.find('div', {'class': 'ContentWrap tabItems'}) 이렇게 바꾸었었습니다.
                # PC의 설정된 환경 혹은 OS플랫폼에 따라서 ContentWrap tabItems의 띄어쓰기가 인식이

                Medal = bs.find('div', {'class': 'SideContent'})
                RankMedal = Medal.findAll('img', {'src': re.compile(
                    '\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
                # Variable RankMedal's index 0 : Solo Rank
                # Variable RankMedal's index 1 : Flexible 5v5 rank

                # for mostUsedChampion
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

                # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

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

        except AttributeError as e:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Non existing Summoner ", embed=embed)

    if message.content.startswith("!레식전적"):

        # Get player nickname and parse page
        playerNickname = ''.join((message.content).split(' ')[1:])
        html = requests.get(playerSite + playerNickname + '/pc/').text
        bs = BeautifulSoup(html, 'html.parser')

        # 한번에 검색 안되는 경우에는 해당 반환 리스트의 길이 존재. -> bs.find('div',{'class' : 'results'}

        if bs.find('div', {'class': 'results'}) == None:
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

                # Add player's MMR Rank MMR Information
                playerInfoMenus = bs.find('a', {'class': 'player-tabs__season_stats'})['href']
                mmrMenu = r6URL + playerInfoMenus
                html = requests.get(mmrMenu).text
                bs = BeautifulSoup(html, 'html.parser')

                # recent season rank box
                # Rank show in purpose : America - Europe - Asia. This code only support Asia server's MMR
                getElements = bs.find('div', {'class': 'card__content'})  # first elements with class 'card__contet is latest season content box

                for ckAsia in getElements.findAll('div', {'class': 'season-stat--region'}):
                    checkRegion = ckAsia.find('div',{'class' : 'season-stat--region-title'}).text
                    if checkRegion == "Asia":
                        getElements = ckAsia
                        break
                    else:
                        pass

                #Player's Tier Information
                latestSeasonTier = getElements.find('img')['alt']
                # MMR Datas Info -> [Win,Losses,Abandon,Max,W/L,MMR]
                mmrDatas = []
                for dt in getElements.findAll('span', {'class': 'season-stat--region-stats__stat'}):
                    mmrDatas.append(dt.text)

                embed = discord.Embed(title="Rainbow Six Siege player search from r6stats", description="",
                                      color=0x5CD1E5)
                embed.add_field(name="Player search from r6stats", value=playerSite + playerNickname + '/pc/',
                                inline=False)
                embed.add_field(name="Player's basic information",
                                value="Ranking : #" + latestSeasonRanking + " | " + "Level : " + playerLevel,
                                inline=False)
                embed.add_field(name="Latest season information | Operation : " + OperationName,
                                value=
                                "Tier(Asia) : " + latestSeasonTier + " | W/L : " + mmrDatas[0] + "/" + mmrDatas[
                                    1] + " | " + "MMR(Asia) : " + mmrDatas[-1],
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
            searchLink = bs.find('a', {'class': 'result'})
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
                bs = BeautifulSoup(html, 'html.parser')
                # Get latest season's Rank information
                latestSeason = bs.findAll('div', {'class': re.compile('season\-rank operation\_[A-Za-z_]*')})[0]

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

                    #Add player's MMR Rank MMR Information
                    playerInfoMenus = bs.find('a', {'class' : 'player-tabs__season_stats'})['href']
                    mmrMenu = r6URL + playerInfoMenus
                    html = requests.get(mmrMenu).text
                    bs = BeautifulSoup(html, 'html.parser')

                    #recent season rank box
                    # Rank show in purpose : America - Europe - Asia. This code only support Asia server's MMR
                    getElements = bs.find('div', {'class': 'card__content'})  # first elements with class 'card__contet is latest season content box

                    for ckAsia in getElements.findAll('div', {'class': 'season-stat--region'}):
                        checkRegion = ckAsia.find('div', {'class': 'season-stat--region-title'}).text
                        if checkRegion == "Asia":
                            getElements = ckAsia
                            break
                        else:
                            pass

                    # Player's Tier Information
                    latestSeasonTier = getElements.find('img')['alt']
                    # MMR Datas Info -> [Win,Losses,Abandon,Max,W/L,MMR]
                    mmrDatas = []
                    for dt in getElements.findAll('span', {'class': 'season-stat--region-stats__stat'}):
                        mmrDatas.append(dt.text)

                    embed = discord.Embed(title="Rainbow Six Siege player search from r6stats", description="",
                                          color=0x5CD1E5)
                    embed.add_field(name="Player search from r6stats", value=searchLink,
                                    inline=False)
                    embed.add_field(name="Player's basic information",value= "Ranking : #" + latestSeasonRanking + " | " + "Level : " + playerLevel,inline=False)
                    embed.add_field(name="Latest season information | Operation : " + OperationName,
                                    value=
                                    "Tier(Asia) : " + latestSeasonTier + " | W/L : " + mmrDatas[0] + "/"+mmrDatas[1] + " | " + "MMR(Asia) : " + mmrDatas[-1],
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

            embed.add_field(name="To see more stats by operator click link here", value=playerOperatorMenu, inline=False)

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
                        mostOperator = convertToNormalEnglish(statlist[0].lower())
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
                embed.add_field(name="To see more stats by operator click link here", value=playerOperatorMenu,
                                inline=False)

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
                            mostOperator = convertToNormalEnglish(statlist[0].lower())
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
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        # 주요 브리핑 및 뉴스링크
        briefTasks = []
        mainbrief = bs.findAll('a', {'href': re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)
        print(briefTasks)

        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
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
        embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0], value="Link : " + briefTasks[0][1], inline=False)
        embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1], inline=False)
        embed.set_thumbnail(
            url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Covid-19 Virus Korea Status", embed=embed)

    if message.content.startswith('!메이플'):

        # Maplestroy base link
        mapleLink = "https://maplestory.nexon.com"
        # Maplestory character search base link
        mapleCharacterSearch = "https://maplestory.nexon.com/Ranking/World/Total?c="
        mapleUnionLevelSearch = "https://maplestory.nexon.com/Ranking/Union?c="


        playerNickname = ''.join((message.content).split(' ')[1:])
        html = urlopen(mapleCharacterSearch + quote(playerNickname))  # Use quote() to prevent ascii error
        bs = BeautifulSoup(html, 'html.parser')

        html2 = urlopen(mapleUnionLevelSearch + quote(playerNickname))
        bs2 = BeautifulSoup(html2,'html.parser')

        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
            embed.add_field(name="Player nickname not entered",
                            value="To use command !메이플 : !메이플 (Nickname)", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Incorrect command usage ", embed=embed)

        elif bs.find('tr', {'class': 'search_com_chk'}) == None:
            embed = discord.Embed(title="Nickname not exist", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 플레이어가 존재하지 않습니다.", value="플레이어 이름을 확인해주세요", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Nickname not exist ", embed=embed)

        else:
            # Get to the character info page
            characterRankingLink = bs.find('tr', {'class': 'search_com_chk'}).find('a', {'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*')})['href']
            #Parse Union Level
            characterUnionRanking = bs2.find('tr', {'class': 'search_com_chk'})
            if characterUnionRanking == None:
                pass
            else:
                characterUnionRanking = characterUnionRanking.findAll('td')[2].text
            html = urlopen(mapleLink + characterRankingLink)
            bs = BeautifulSoup(html, 'html.parser')

            # Find Ranking page and parse page
            personalRankingPageURL = bs.find('a', {'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*\/Ranking\?p\=[A-Za-z0-9%?=]*')})['href']
            html = urlopen(mapleLink + personalRankingPageURL)
            bs = BeautifulSoup(html, 'html.parser')
            #Popularity

            popularityInfo = bs.find('span',{'class' : 'pop_data'}).text.strip()
            ''' Can't Embed Character's image. Gonna fix it after patch note
            #Character image
            getCharacterImage = bs.find('img',{'src': re.compile('https\:\/\/avatar\.maplestory\.nexon\.com\/Character\/[A-Za-z0-9%?=/]*')})['src']
            '''
            infoList = []
            # All Ranking information embeded in <dd> elements
            RankingInformation = bs.findAll('dd')  # [level,job,servericon,servername,'-',comprehensiveRanking,'-',WorldRanking,'-',JobRanking,'-',Popularity Ranking,'-',Maple Union Ranking,'-',Achivement Ranking]
            for inf in RankingInformation:
                infoList.append(inf.text)
            embed = discord.Embed(title="Player " + playerNickname + "'s information search from nexon.com", description=infoList[0] + " | " +infoList[1] + " | " + "Server : " + infoList[2], color=0x5CD1E5)
            embed.add_field(name="Click on the link below to view more information.", value = mapleLink + personalRankingPageURL, inline=False)
            embed.add_field(name="Overall Ranking",value=infoList[4], inline=True)
            embed.add_field(name="World Ranking", value=infoList[6], inline=True)
            embed.add_field(name="Job Ranking", value=infoList[8], inline=True)
            embed.add_field(name="Popularity Ranking", value=infoList[10] + "( " +popularityInfo + " )", inline=True)
            if characterUnionRanking == None:
                embed.add_field(name="Maple Union", value=infoList[12],inline=True)
            else:
                embed.add_field(name="Maple Union", value=infoList[12] + "( LV." + characterUnionRanking + " )", inline=True)
            embed.add_field(name="Achivement Ranking", value=infoList[14], inline=True)
            embed.set_thumbnail(url='https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png')
            embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Player " + playerNickname +"'s information search", embed=embed)

    if message.content.startswith("!한영번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        #띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ko&target=en&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> English", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated English", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")


    if message.content.startswith("!영한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=en&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | English -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="English to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!한일번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ko&target=ja&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Japanese", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Japanese", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!일한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ja&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Japanese -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="Japanese to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!한중번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.

                #Simplified Chinese
                dataParmas = "source=ko&target=zh-CN&text=" + combineword

                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Chinese(Simplified Chinese)", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Chinese(Simplified)", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!중한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                # Simplified Chinese
                dataParmas = "source=zh-CN&target=ko&text=" + combineword


                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Chinese -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="Chinese to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",
                                     icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!배그솔로1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !배그솔로 : !배그솔로 (Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                soloQueInfo = bs.find('section', {'class': "solo modeItem"})
                if soloQueInfo == None:
                    embed = discord.Embed(title="Not existing plyer",description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",color=0x5CD1E5)
                    await message.channel.send("Error : Not existing player", embed=embed)
                else:
                    soloQueInfo = soloQueInfo.find('div', {'class': "mode-section tpp"})
                    if soloQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s TPP solo que information",
                                                   embed=embed)
                    else:
                        # print(soloQueInfo)
                        # Get total playtime
                        soloQueTotalPlayTime = soloQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        soloQueGameWL = soloQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = soloQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = soloQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        print(tierImage)
                        tier = tierInfos['alt']

                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in soloQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(ci.text.strip())
                        comInfopercentage = []
                        # [전체 상위 %, K/D,승률,Top10,평균딜량,게임수,최다킬수,헤드샷,저격,생존,None]
                        for cif in soloQueInfo.findAll('span', {'class': 'top'}):
                            comInfopercentage.append((cif.text))

                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg",
                                              description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server",
                                        value=seasonInfo[2] + " Server / Total playtime : " + soloQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier / Top Rate / Average Rank",
                                        value=tier + " (" + rankPoint + "p)" + " / " + comInfopercentage[0] + " / " +
                                              comInfo[-1], inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] + "/" + comInfopercentage[1], inline=True)
                        embed.add_field(name="승률", value=comInfo[1] + "/" + comInfopercentage[2], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] + "/" + comInfopercentage[3], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] + "/" + comInfopercentage[4], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판/" + comInfopercentage[5], inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬/" + comInfopercentage[6], inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] + "/" + comInfopercentage[7], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] + "/" + comInfopercentage[8], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] + "/" + comInfopercentage[9], inline=True)
                        embed.set_thumbnail(url=tierImage)
                        embed.set_footer(text='Service provided by Hoplin.',
                                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send(
                            "PUBG player " + playerNickname + "'s " + seasonInfo[1] + " TPP solo que information",
                            embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer", description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",color=0x5CD1E5)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("!배그듀오1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !배그스쿼드 : !배그스쿼드 (Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                duoQueInfo = bs.find('section',{'class' : "duo modeItem"})
                if duoQueInfo == None:
                    embed = discord.Embed(title="Not existing plyer",
                                          description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                          color=0x5CD1E5)
                    await message.channel.send("Error : Not existing player", embed=embed)
                else:
                    duoQueInfo = duoQueInfo.find('div',{'class' : "mode-section tpp"})
                    if duoQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Duo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s TPP duo que information",
                                                   embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        duoQueTotalPlayTime = duoQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        duoQueGameWL = duoQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = duoQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = duoQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']

                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in duoQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(ci.text.strip())
                        comInfopercentage = []
                        # [전체 상위 %, K/D,승률,Top10,평균딜량,게임수,최다킬수,헤드샷,저격,생존,None]
                        for cif in duoQueInfo.findAll('span', {'class': 'top'}):
                            comInfopercentage.append((cif.text))

                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg",
                                              description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server and total playtime",
                                        value=seasonInfo[2] + " Server / Total playtime : " + duoQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point) / Top Rate / Average Rank",
                                        value=tier + " (" + rankPoint + "p)" + " / " + comInfopercentage[0] + " / " +
                                              comInfo[-1], inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] + "/" + comInfopercentage[1], inline=True)
                        embed.add_field(name="승률", value=comInfo[1] + "/" + comInfopercentage[2], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] + "/" + comInfopercentage[3], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] + "/" + comInfopercentage[4], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판/" + comInfopercentage[5], inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬/" + comInfopercentage[6], inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] + "/" + comInfopercentage[7], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] + "/" + comInfopercentage[8], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] + "/" + comInfopercentage[9], inline=True)
                        embed.set_thumbnail(url=tierImage)
                        embed.set_footer(text='Service provided by Hoplin.',
                                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send(
                            "PUBG player " + playerNickname + "'s " + seasonInfo[1] + " TPP duo que information",
                            embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x5CD1E5)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("!배그스쿼드1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !배그솔로 : !배그솔로 (Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                squadQueInfo = bs.find('section',{'class' : "squad modeItem"})
                if squadQueInfo == None:
                    embed = discord.Embed(title="Not existing plyer",
                                          description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                          color=0x5CD1E5)
                    await message.channel.send("Error : Not existing player", embed=embed)
                else:
                    squadQueInfo = squadQueInfo.find('div',{'class' : "mode-section tpp"})
                    if squadQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Squad que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send(
                            "PUBG player " + playerNickname + "'s " + seasonInfo[1] + " TPP squad que information",
                            embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        squadQueTotalPlayTime = squadQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        squadQueGameWL = squadQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = squadQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = squadQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']

                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in squadQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(ci.text.strip())
                        comInfopercentage = []
                        # [전체 상위 %, K/D,승률,Top10,평균딜량,게임수,최다킬수,헤드샷,저격,생존,None]
                        for cif in squadQueInfo.findAll('span', {'class': 'top'}):
                            comInfopercentage.append((cif.text))

                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg",
                                              description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server",
                                        value=seasonInfo[2] + " Server / Total playtime : " + squadQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point) / Top Rate / Average Rank",
                                        value=tier + " (" + rankPoint + "p)" + " / " + comInfopercentage[0] + " / " +
                                              comInfo[-1], inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] + "/" + comInfopercentage[1], inline=True)
                        embed.add_field(name="승률", value=comInfo[1] + "/" + comInfopercentage[2], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] + "/" + comInfopercentage[3], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] + "/" + comInfopercentage[4], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판/" + comInfopercentage[5], inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬/" + comInfopercentage[6], inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] + "/" + comInfopercentage[7], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] + "/" + comInfopercentage[8], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] + "/" + comInfopercentage[9], inline=True)
                        embed.set_thumbnail(url=tierImage)
                        embed.set_footer(text='Service provided by Hoplin.',
                                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send(
                            "PUBG player " + playerNickname + "'s " + seasonInfo[1] + " TPP squad que information",
                            embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x5CD1E5)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("!배그솔로2"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !배그솔로 : !배그솔로 (Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                soloQueInfo = bs.find('section', {'class': "solo modeItem"})
                if soloQueInfo == None:
                    embed = discord.Embed(title="Not existing plyer",
                                          description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                          color=0x5CD1E5)
                    await message.channel.send("Error : Not existing player", embed=embed)
                else:
                    soloQueInfo = soloQueInfo.find('div', {'class': "mode-section fpp"})
                    if soloQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s FPP solo que information",
                                                   embed=embed)
                    else:
                        # print(soloQueInfo)
                        # Get total playtime
                        soloQueTotalPlayTime = soloQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        soloQueGameWL = soloQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = soloQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = soloQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        print(tierImage)
                        tier = tierInfos['alt']

                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in soloQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(ci.text.strip())
                        comInfopercentage = []
                        # [전체 상위 %, K/D,승률,Top10,평균딜량,게임수,최다킬수,헤드샷,저격,생존,None]
                        for cif in soloQueInfo.findAll('span', {'class': 'top'}):
                            comInfopercentage.append((cif.text))

                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg",
                                              description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server",
                                        value=seasonInfo[2] + " Server / Total playtime : " + soloQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier / Top Rate / Average Rank",
                                        value=tier + " (" + rankPoint + "p)" + " / " + comInfopercentage[0] + " / " +
                                              comInfo[-1], inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] + "/" + comInfopercentage[1], inline=True)
                        embed.add_field(name="승률", value=comInfo[1] + "/" + comInfopercentage[2], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] + "/" + comInfopercentage[3], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] + "/" + comInfopercentage[4], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판/" + comInfopercentage[5], inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬/" + comInfopercentage[6], inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] + "/" + comInfopercentage[7], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] + "/" + comInfopercentage[8], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] + "/" + comInfopercentage[9], inline=True)
                        embed.set_thumbnail(url=tierImage)
                        embed.set_footer(text='Service provided by Hoplin.',
                                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send(
                            "PUBG player " + playerNickname + "'s " + seasonInfo[1] + " FPP solo que information",
                            embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x5CD1E5)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("!배그듀오2"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !배그스쿼드 : !배그스쿼드 (Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                duoQueInfo = bs.find('section', {'class': "duo modeItem"})
                if duoQueInfo == None:
                    embed = discord.Embed(title="Not existing plyer",
                                          description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                          color=0x5CD1E5)
                    await message.channel.send("Error : Not existing player", embed=embed)
                else:
                    duoQueInfo = duoQueInfo.find('div', {'class': "mode-section fpp"})
                    if duoQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Duo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s FPP duo que information",
                                                   embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        duoQueTotalPlayTime = duoQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        duoQueGameWL = duoQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = duoQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = duoQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']

                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in duoQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(ci.text.strip())
                        comInfopercentage = []
                        # [전체 상위 %, K/D,승률,Top10,평균딜량,게임수,최다킬수,헤드샷,저격,생존,None]
                        for cif in duoQueInfo.findAll('span', {'class': 'top'}):
                            comInfopercentage.append((cif.text))

                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg",
                                              description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server and total playtime",
                                        value=seasonInfo[2] + " Server / Total playtime : " + duoQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point) / Top Rate / Average Rank",
                                        value=tier + " (" + rankPoint + "p)" + " / " + comInfopercentage[0] + " / " +
                                              comInfo[-1], inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] + "/" + comInfopercentage[1], inline=True)
                        embed.add_field(name="승률", value=comInfo[1] + "/" + comInfopercentage[2], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] + "/" + comInfopercentage[3], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] + "/" + comInfopercentage[4], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판/" + comInfopercentage[5], inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬/" + comInfopercentage[6], inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] + "/" + comInfopercentage[7], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] + "/" + comInfopercentage[8], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] + "/" + comInfopercentage[9], inline=True)
                        embed.set_thumbnail(url=tierImage)
                        embed.set_footer(text='Service provided by Hoplin.',
                                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send(
                            "PUBG player " + playerNickname + "'s" + seasonInfo[1] + "FPP duo que information",
                            embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x5CD1E5)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("!배그스쿼드2"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !배그솔로 : !배그솔로 (Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                squadQueInfo = bs.find('section', {'class': "squad modeItem"})
                if squadQueInfo == None:
                    embed = discord.Embed(title="Not existing plyer",
                                          description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                          color=0x5CD1E5)
                    await message.channel.send("Error : Not existing player", embed=embed)
                else:
                    squadQueInfo = squadQueInfo.find('div',{'class': "mode-section fpp"})
                    if squadQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Squad que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s FPP squad que information",
                                                   embed=embed)
                    else:
                        # Get total playtime
                        squadQueTotalPlayTime = squadQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        squadQueGameWL = squadQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = squadQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = squadQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']

                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in squadQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(ci.text.strip())
                        comInfopercentage = []
                        # [전체 상위 %, K/D,승률,Top10,평균딜량,게임수,최다킬수,헤드샷,저격,생존,None]
                        for cif in squadQueInfo.findAll('span', {'class': 'top'}):
                            comInfopercentage.append((cif.text))

                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg",
                                              description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server",
                                        value=seasonInfo[2] + " Server / Total playtime : " + squadQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point) / Top Rate / Average Rank",
                                        value=tier + " (" + rankPoint + "p)" + " / " + comInfopercentage[0] + " / " +
                                              comInfo[-1], inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] + "/" + comInfopercentage[1], inline=True)
                        embed.add_field(name="승률", value=comInfo[1] + "/" + comInfopercentage[2], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] + "/" + comInfopercentage[3], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] + "/" + comInfopercentage[4], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판/" + comInfopercentage[5], inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬/" + comInfopercentage[6], inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] + "/" + comInfopercentage[7], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] + "/" + comInfopercentage[8], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] + "/" + comInfopercentage[9], inline=True)
                        embed.set_thumbnail(url=tierImage)
                        embed.set_footer(text='Service provided by Hoplin.',
                                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send("PUBG player " + playerNickname + "'s " + seasonInfo[1] + " FPP squad que information",embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x5CD1E5)
            await message.channel.send("Error : Not existing player", embed=embed)
client.run(bottoken)
