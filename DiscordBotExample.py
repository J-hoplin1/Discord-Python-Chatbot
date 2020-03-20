import discord, asyncio,sys


token = "" # Token Here from Bot Admin Page
client = discord.Client() # use Client
@client.event
async def on_ready(): # do action 1 time when ready

    # discord.Status.online -> dnd : "다른 용무 중", idle : "자리 비움"
    await client.change_presence(status=discord.Status.online, activity=discord.Game("")) # print status at right of discord UI
    print("I'm Ready!") # print state
    print(client.user.name) # print bot name.
    print(client.user.id) # print bot's id.

@client.event
async def on_message(message): # do action when message sent
    if message.author.bot: # if chatter is bot
        return None # do not react
    print(message.content)
    if message.content.startswith("!명령어"): # if user send message !명령어
        embed = discord.Embed(title="명령어",description="명령어 목록",color=0x5CD1E5) #embed box to emphasize or show more details
        await message.channel.send("명령어 목록이에요!",embed=embed)
        # To user who sent message
        #await message.author.send("응답")

    if message.content.startswith("!개발자"):
        embed = discord.Embed(title="이 챗봇의 개발자 정보와 호스팅 위치",description="!ㅡ!",color=0x1BF1E6)
        embed.set_image(url="https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4") # to embed image at embeded box
        embed.add_field(name="개발자 : Hoplin",value="https://github.com/J-hoplin1",inline=False) # make a field at box
        embed.add_field(name="서버 호스팅",value="Hosted by AWS. With Ubuntu, using version 16.04 LTS",inline=False)
        embed.add_field(name="호스팅 위치",value="Commonwealth of Virginia, USA",inline=False)
        embed.add_field(name="사용된 API와 언어",value="Discord APIs, with Python3", inline=False)
        await message.channel.send("!",embed=embed) # send Message to Channel

    if message.content.startswith("!넌누구니"):
        await message.channel.send("삐리리릭! 저는 지구 정복이 꿈인 기여운 도우미봇이에오! \ㅇ∀ㅇ/")

client.run(token) # Discord Bot will log in your channel with token you give.