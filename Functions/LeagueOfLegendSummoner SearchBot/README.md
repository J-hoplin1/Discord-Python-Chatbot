Discord Bot : League of Legend player information search bot
===
***
1 . Discord.py Version : 1.0.0(Rewrite Version)

2 . Language : Python3

3 . What for? : To make able to see summoner's information URL, Rank Info, Most Champion with using command

4 . Warning  : This Application is only available for South Korea. I'm gonna make other countries' server able to use it.
***

- How to Use?

    - I'll wrtie how to use based on you just add bot application to your discord server.

    - Copy your bot's token from your bot admin page.

        ```python3
        def deleteTags(htmls):
        for a in range(len(htmls)):
            htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
        return htmls

        bottoken = ''

        @client.event # Use these decorator to register an event.
        async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
        await client.change_presence(status=discord.Status.online, activity=discord.Game("수리중"))
        print("New log in as {0.user}".format(client))
        ```

    - And pasted your token to variable 'bottoken'(ln[77] in code). Token should be valued as string types. 

    - Run Code.
    
    - To use command
    
        ~~~
            !롤전적 (player nickname)
        ~~~

    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/1.PNG?raw=true)

    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/2.PNG?raw=true)
    
    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/3.PNG?raw=true)
    
    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/4.PNG)
