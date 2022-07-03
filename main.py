from EmbedGenerator import EmbedGenerator


try:
    from VNDB import VNDB
    from discord.ext import commands
    from utils import deleteMessage, getFinalFlag,inputRequest,checkIfNameRight,getMainParameter,getMainFromFilters
    from EmbedGenerator import EmbedGenerator
    from Error import *
except Exception as e:
    print(e)


bot = commands.Bot(command_prefix='!')

global vndb

try:
    vndb = VNDB('test',1.0,'Flender',None,True)
    embedGen = EmbedGenerator(vndb)
except Exception as e:
    print(e)


#page1 = vndb.get('vn', 'basic', '(title~"c")', '')
#page2 = vndb.get('vn', 'basic', '(title~"c")', '(page=2)')
#test = vndb.get('quote', 'basic', "(id>=1)",'{"results":1}')
#test = vndb.get('vn', 'basic,stats', '(title~"c")', '{"sort":"popularity","reverse":true}')
#test = vndb.get('vn', 'basic', '(id = [1,2,3])', '')

#print(test)


#print(page1)
#print(page2)

#details

@bot.command()
async def search(ctx,*parameters):

    """
    The command for start the research.
    Give me just your type of research and the name.
    Exemple: !search <vn/character> CLANNAD
    """

    # Delete the commande message
    await deleteMessage(ctx,1)

    # Check if search global
    if (parameters[0].lower() not in ['vn','character']):
        await ctx.send(MSG_FONCTIONNALITY_NOT_CODE)
    
    # Check if search with type
    else:

        # Extract parameters from command
        name = " ".join(parameters[1:len(parameters)])
        type = parameters[0]

        # Prepare request with type
        if type == 'vn':
            request = vndb.get(type,'basic','('+ getMainParameter(type) +'~"' + name +'")','{"sort":"popularity","reverse":true}')
        else:
            request = vndb.get(type,'basic','('+ getMainParameter(type) +'~"' + name +'")','')

        # Check if request contain the exact name
        if checkIfNameRight(request['items'],getMainParameter(type),name) != None or request['num'] == 1:
            fullRequest = vndb.get(type,getFinalFlag(type),f"(id={request['items'][0]['id']})",'')
            await ctx.send(embed=embedGen.createEmbed(type,fullRequest['items'][0]))

        # Ckeck if there are many result of request
        elif request['num'] > 1:
            
            # Send a embed list to choose in list
            await ctx.send(embed=embedGen.generateEmbedListSimple(type,name,request['items'],1))

            # Initialise while
            rep = 'page'
            find = False

            # While object not find or changing page
            while not find and rep.split(' ')[0].lower() == 'page':
            
                # Ask a new response
                rep = await inputRequest(ctx,bot)
                
                # Create a list to choose with word
                repLs = str(rep).lower().split(' ')
                
                await deleteMessage(ctx,2)

                # If response is a number, choose the object with the id
                if repLs[0].isdigit():
                    nb = int(repLs[0])
                    if (nb >= 1 and nb <= len(request['items'])):
                        fullRequest = vndb.get(type,getFinalFlag(type),f"(id={request['items'][nb-1]['id']})",'')
                        await ctx.send(embed=embedGen.createEmbed(type,fullRequest['items'][0]))
                        find = True
                    else:
                        await ctx.send(MSG_NUMBER_NOT_INT_RANGE)
            
                # If response is cancel, cancel request
                elif repLs[0] == 'cancel':
                    await ctx.send(MSG_REQUESTS_CANCEL)
                    find = True

                # If response is page [x] , go to the page[x]
                elif repLs[0] == 'page':
                    
                    # Prepare new request with page chagement
                    if type == 'vn':
                        request = vndb.get(type,'basic','('+ getMainParameter(type) +'~"' + name +'")','{"sort":"popularity","reverse":true,"page":'+str(repLs[1])+'}')
                    else:
                        request = vndb.get(type,'basic','('+ getMainParameter(type) +'~"' + name +'")','{"page":'+str(repLs[1])+'}')

                    
                    await ctx.send(embed=embedGen.generateEmbedListSimple(type,name,request['items'],repLs[1]))
            
                else:
                    await ctx.send(MSG_INPUT_NOT_CORRECT)

        else:
            await ctx.send(MSG_NOTHING_FOUND)

@bot.command()
async def randomquote(ctx):

    """
    I have a quote for you
    """

    await deleteMessage(ctx,1)
    quote = vndb.get('quote', 'basic', "(id>=1)",'{"results":1}')['items'][0]
    await ctx.send(embed=embedGen.createEmbed('quote',quote))


@bot.command()
async def randomvn(ctx):

    """
    I can choose a VN just for you !
    """

    await deleteMessage(ctx,1)
    #vn = vndb.get('vn', 'basic,details,stats', "(id>=1)",'{"results":1}')['items'][0]
    #await ctx.send(embed=embedGen.createEmbed('vn',vn))
    await ctx.send('Not working for now...')

@bot.command()
async def info(ctx):
    
    """
    I can present myself I you want !
    """
    
    await deleteMessage(ctx,1)
    await ctx.send("Hello, nice to meet you. I'm Chihiro Fujisaki...\nSorry, I get kinda embarrassed whenever I introduce myself like this...\nAnyway, I hope we can get along...\n" +
        "I'm here to help you to find VN or character.\nI search on the API of VNDB, there are a lot of games here.\nI hope I can be useful for you...nIf you want to know how I work, call me with !help.")



bot.run('YOUR-TOKEN')