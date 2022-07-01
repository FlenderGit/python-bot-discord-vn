from random import choice
import discord
import aiohttp
import asyncio

from discord.ext import commands,tasks
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix='!')

def createFicheFromHTML ( html:str ) -> discord.Embed:

    """
    Function createFicheFromHTML ( html : str ) : Embed
    Create a embed from a html page of vndb
    """

    soup = BeautifulSoup(html,features="html.parser")

    name = soup.find("div", {"id":"maincontent"}).find("div",{"class":"mainbox"}).find("h1").get_text()
    thumbnail = soup.find("div", {"id":"maincontent"}).find("div",{"class":"mainbox"}).find("div",{"class":"vndetails"}).find("div",{"class":"vnimg"}).find("label",{"class":"imghover"}).find("div",{"class":"imghover--visible"}).find("img")['src']
    description = soup.find("div", {"id":"maincontent"}).find("div",{"class":"mainbox"}).find("div",{"class":"vndetails"}).find("table",{"class":"stripe"}).find("tr",{"class":"nostripe"}).find("td",{"class":"vndesc"}).find("p").get_text()

    if len(description) > 1024:
        description = description[:1010] + "..."

    embed = discord.Embed(title="Recherche de : "+ name)
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="Description :", value=description, inline=False)
    embed.add_field(name="Link :", value=soup.find('base')['href'], inline=True)

    return embed

def numeralToStr (i:int)->str:

    """
    Function numeralToStr ( i = int) : str
    Transform a number intohis str 
    Exemple : 1 -> 'one'
    """

    r = ""

    if ( i == 1 ):
        r = "one"
    elif ( i == 2 ):
        r = "two"
    elif ( i == 3 ):
        r = "three"
    elif ( i == 4 ):
        r = "four"
    elif ( i == 5 ):
        r = "five"
    elif ( i == 6 ):
        r = "six"
    elif ( i == 7 ):
        r = "seven"
    elif ( i == 8 ):
        r = "eight"
    elif ( i == 9 ):
        r = "nine"

    return r

# Command search
@bot.command()
async def search(ctx,*name):

    nameWithSpace = " ".join(name)
    await ctx.channel.purge(limit=1)

    print(ctx.author.display_name + " use !search")
    print( nameWithSpace + " = https://vndb.org/v?q=" + "+".join(name) + "&s=33A\n")

    async with aiohttp.ClientSession() as session:
        async with session.get("https://vndb.org/v?q=" + "+".join(name) + "&s=33A" ) as response:
            
            if  response.status == 200:

                html = await response.text()
                soup = BeautifulSoup(html,features="html.parser")

                # AF : Test si direct page
                if soup.find('title').get_text() == 'Browse visual novels | vndb':
                
                    if ( soup.find("div", {"id":"maincontent"}).find("div",{"class":"mainbox browse vnbrowse"}) != None ):

                        divGames = soup.find("div", {"id":"maincontent"}).find("div",{"class":"mainbox browse vnbrowse"}).find("table").find_all("tr")[1::]

                        find = False
                        i = 0

                        lenght = len(divGames)

                        # Test if game is in list
                        while i < lenght and not find :
                        
                            if divGames[i].a.get_text().upper() == nameWithSpace.upper():
                                find = True
                            else:
                                i += 1

                        # If find in list
                        if find:

                            div = divGames[i]

                            async with session.get("https://vndb.org" + div.a['href'] ) as responseInfo:

                                if  responseInfo.status == 200:

                                    htmlGame = await responseInfo.text()
                                    embed = createFicheFromHTML(htmlGame)
                                    embed.set_author(name="Request by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
                                    await ctx.send(embed=embed)
                                    
                                else:
                                    print("ERROR : URL " + "https://vndb.org" + div.a['href'] + " DON'T WORK")

                        # If not find in list
                        else:

                            ls = ""
                            gameLs = []


                            for i in range(lenght):
                                game = divGames[i]
                                nameGame = game.a.get_text()

                                if ( len(nameGame) >= 50 ):
                                    nameGame = nameGame[:50] + "..."

                                gameLs.append(game.a['href'])

                                ls += str(i+1) + ". " + nameGame + "\n\n"

                            embed = discord.Embed(title= " ".join(name) + " not find... Are you looking for? ?",description=ls)
                            embed.set_author(name="Request by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)

                            await ctx.send(embed=embed)

                            def check(msg):
                                return msg.author == ctx.author and msg.channel == ctx.channel

                            # Interaction with list
                            try:
                                msg = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
                                await ctx.channel.purge(limit=2)

                                txt = msg.content

                                if txt.isdigit():
                                    nb = int(txt)
                                    if ( nb > 0 and nb <= lenght ):

                                        async with session.get("https://vndb.org" + gameLs[nb-1] ) as responseInfo:

                                            if  responseInfo.status == 200:

                                                html = await responseInfo.text()
                                                embed = createFicheFromHTML(html)
                                                embed.set_author(name="Request by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
                                                await ctx.send(embed=embed)

                                            else:
                                                print("")

                                    else:
                                        await ctx.send("This number is not in the list")

                                elif txt.upper() == 'CANCEL' :
                                    await ctx.send("You have cancel the research")

                                else:
                                    await ctx.send("This is not a number")

                            # Interection with list too long
                            except asyncio.TimeoutError:
                                await ctx.send("Sorry, you didn't reply in time!")

                    # Research doesn't have result
                    else:
                        await ctx.send(nameWithSpace + " don't have result")
                
                # Research into game directly
                else:
                    embed = createFicheFromHTML(html)
                    embed.set_author(name="Request by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

            # Page search not found       
            else:
                print("PAGE NOT FOUND : " + response.status)

@bot.command()
async def vnrand(ctx):
    print(ctx.author.display_name + " use !vrand\n")
    await ctx.channel.purge(limit=1)
    async with aiohttp.ClientSession() as session:
        async with session.get("https://vndb.org/v/rand") as response:
            if  response.status == 200:
                embed = createFicheFromHTML(await response.text())
                await ctx.send(embed=embed)
            else:
                print("PAGE NOT FOUND : " + response.status) 

@bot.command()
async def hello(ctx):
    print(ctx.author.display_name + " use !hello\n")
    await ctx.channel.purge(limit=1)
    await ctx.send("Hello, nice to meet you. I'm Chihiro Fujisaki...\nSorry, I get kinda embarrassed whenever I introduce myself like this...\nAnyway, I hope we can get along...")


lsStatus = [ "Helping peoples !"]

@tasks.loop(minutes = 30)
async def statusChange():
    await bot.change_presence(activity=discord.Game(name=choice(lsStatus)))

statusChange.before_loop(bot.wait_until_ready)   
statusChange.start()

bot.run('OTkyMDMxMDI1NTIzODUxMzUz.GpL_vQ.DQZ0oUkzzdua-OpBp8KBnwauTsOXCqa-idU7nU')