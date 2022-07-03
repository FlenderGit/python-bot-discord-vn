from asyncio import TimeoutError
from Error import MSG_INPUT_TIMEOUT

def convertLandToEmoticon( land : str ) -> str:

    r = ""

    if ( land =='ja' ):
        r = ":flag_jp:"
    elif ( land == 'ko' ):
        r = ":flag_kr:"
    elif ( land == 'fr' ):
        r = ":flag_fr: "
    elif ( land == 'es'):
        r = ":flag_es:"
    elif ( land == 'en' ):
        r = ":flag_gb:"
    elif ( land == 'de' ):
        r = ":flag_de:"
    elif ( land == 'zh-Hans'):
        r = ":flag_cn: _(Trad)_"
    elif ( land == 'zh-Hant'):
        r = ":flag_cn: _(Sim)_"
    elif ( land == 'it'):
        r = ":flag_it:" 
    elif ( land == 'ru'):
        r = ":flag_ru:"
    elif ( land == 'it'):
        r = ":flag_it:"
    elif ( land == 'pt-br'):
        r = ":flag_pt:"      
    elif ( land == 'vi' ):
        r = ":flag_vi:"
    else:
        r = land

    return r

def getMainParameter(type:str)->str:

    r = ""

    if ( type == 'vn' or type == 'quote' ):
        r = 'title'
    elif ( type == 'character'):
        r = 'name'
    
    return r

async def deleteMessage (ctx,nb:1)->None:
    await ctx.channel.purge(limit=nb)

def checkIfNameRight(data:list,mainParameter:str,lookingFor)->dict:
    
    """
    Function checkIfNameRight(data:list,mainParameter:str,lookingFor:str)->dict
    Usage: Check if there are a object if a list with the first parameter equals to what we looking for
    Parameters: 
        data : the list of object
        mainParameter : the main parameter of the list of object ( Ex : vn = title , character = name ... )
        lookingFor : the name of what's we looking for
    Return: the dict of the object if it's in list or None
    """

    r = None

    lenght = len(data)
    i = 0
    find = False

    while not find and i < lenght:
            obj = data[i]
            if ( obj[mainParameter].upper() == lookingFor.upper() ):
                find = True
                r = obj
            i+=1

    return r


async def inputRequest(ctx,bot):

    msg = None

    try:
        msg = await bot.wait_for("message", timeout=30) # 30 seconds to reply
        msg = msg.content

    except TimeoutError:
        await ctx.send(MSG_INPUT_TIMEOUT)

    return msg

def getMainFromFilters(filters:str,mainParameter:str):
    if ( mainParameter in  filters):
        start = filters.index(mainParameter)+7
        title = ""
        while filters[start]!='"' and start < len(filters):
            title +=filters[start]
            start+=1
    return title

def getFinalFlag(type:str):
    r="basic"
    if(type=='vn'):
        r+=',details,stats'
    elif(type=='character'):
        r+=',details,vns'
    return r

def convertGenderToEmoticon(gender:str):
    r = ''
    if gender == 'f':
        r = ':female_sign: '
    elif gender == 'm':
        r = ':male_sign: '

    return r

def createHyperlink(text:str,link:str)->str:
    return '[' + text + '](' + link + ')'

def translateTypeToStr(type:str)->str:
    if(type=='vn'):
        r='Visual Novel'
    elif(type=='character'):
        r+='Character'
    else:
        r=type
    return r