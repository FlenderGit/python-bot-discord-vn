from discord import Embed
from VNDB import VNDB
from utils import convertLandToEmoticon, getMainParameter,convertGenderToEmoticon,createHyperlink,translateTypeToStr


class EmbedGenerator:

    def __init__(self,VNDB:VNDB) -> None:

        """
        Constructor of EmbedGenerator
        Parameter: VNDB to make other requests if necessery
        """

        self.VNDB = VNDB

    def createEmbed(self,type:str,data:dict)->Embed:

        """
        Methode to create Embed for data of object and his type
        """

        r = ""


        if ( type == 'vn' ):
            embed = Embed(title=data[getMainParameter(type)],description="")
            r = self.createGameEmbed(embed,data)
        elif ( type == 'character'):
            embed = Embed(title=data[getMainParameter(type)])
            r = self.createCharacterEmbed(embed,data)
        elif ( type == 'quote'):
            embed = Embed(title="")
            r = self.createQuoteEmbed(embed,data)

        return r

    def createGameEmbed (self,embed:Embed, game : list ) -> Embed :
        
        # Image
        embed.set_thumbnail(url=game['image'])
        
        # Original name
        embed.add_field(name="Original name :" , value=game['original'],inline=True)
        
        # Original language
        embed.add_field(name="Original language :" , value=convertLandToEmoticon(game['orig_lang'][0]),inline=True)
       
        # Languages of the game
        embed.add_field(name="Language :" , value=" ".join([convertLandToEmoticon(land) for land in game['languages']]),inline=False)

        # Description
        description = game['description']
        if description != None:
            if ( len(description) >= 1000 ):
                description = description[:1000] + "..."
            embed.add_field(name="Description :", value=description, inline=False)

        # Support
        embed.add_field(name="Support :" , value=", ".join([support for support in game['platforms']]),inline=True)
        
        # Link
        embed.add_field(name="Link :", value='https://vndb.org/v'+str(game['id']), inline=True)
        
        return embed

    def createCharacterEmbed (self,embed:Embed, character : list ) -> Embed :

        # Add gender to title
        embed.title += " " + convertGenderToEmoticon(character['gender'])
        
        # Image
        embed.set_thumbnail(url=character['image'])

        # Original name
        if character['original'] != None:
            embed.add_field(name="Original name :" , value=character['original'],inline=True)

        # Other Name
        if character['aliases'] != None:
            embed.add_field(name="Other name :" , value=character['aliases'].replace('\n',', ') if character['aliases'] != None else 'No other name' ,inline=True)
        
        # Game apparition:
        if character['vns'] != None:
            lsGame = self.VNDB.getListGameFromId([vn[0] for vn in character['vns']] )
            embed.add_field(name="Appears in :" , value=", ".join([createHyperlink(game['title'],'https://vndb.org/v'+str(game['id'])) for game in lsGame]),inline=False)

        # Birthday
        if character['birthday'][1] != None and character['birthday'][0] != None:
            embed.add_field(name="Birthday :", value=str(character['birthday'][0]) +"/" + str(character['birthday'][1]), inline=True)
        
        # Description
        description = character['description']
        if ( description != None):
            if 'spoiler' in description:
                    description = description.replace('[spoiler]','SPOILER :warning: :\n||').replace('[/spoiler]','||')
            description.replace('\n\n','\n')
            if ( len(description) >= 1000 ):
                description = description[:1000] + "..."
            embed.add_field(name="Description :", value=description, inline=False)
        else:
            description = 'No description...'

        # Link
        embed.add_field(name="Link :", value='https://vndb.org/c'+str(character['id']), inline=True)

        return embed

    def createListEmbed(self, ls:list,type:str,mainParameter:str)->Embed:
        embed = Embed(title=mainParameter + " not found... Are you looking for ?")

        desc = ""
        for i in range(len(ls)):
            desc += str(i+1) + ". " + ls[i][getMainParameter(type)] + "\n\n"

        embed.description = desc

        return embed

    def createQuoteEmbed(self,embed:Embed,quote:dict):
        embed.description = quote['quote']
        embed.set_footer(text="From " + quote['title'])
        return embed

    def getDescription(self,type:str,data:list)->str:

        r = ''

        if type == 'vn':
            r = self.getVNDescription(data)
        elif type == 'character':
            r = self.getCharacterDescription(data)

        return r

    @staticmethod
    def getVNDescription(data:dict)->str:
        desc = ""
        for i in range(len(data)):
            desc += str(i+1) + ". " + data[i]['title'] + "\n\n"
        return desc

    def getCharacterDescription(self,data:dict)->str:
        desc = ""
        for i in range(len(data)):
            desc += str(i+1) + ". " + data[i]['name'] + "\n\n"
        return desc

    def generateEmbedListSimple(self,type:str,lookingFor:str,data:dict,page:int)->Embed:
        embed = Embed(title=lookingFor + ' not found... Are you looking for ?')
        embed.description = self.getDescription(type,data)
        embed.set_footer(text='Page ' + str(page) + ' - Input the id, page [x], or cancel')
        return embed
