import time
import discord
import requests
import json

from discord.utils import get
from discord.ext.commands import Bot

with open('config.json') as fp:
    config = json.load(fp)
token = config['token']
client = Bot(command_prefix='#')
botversion=config['version']

# Variables
class osrsHiScores(object):
    def __init__(self, user, accType):

        self.user = user
        self.accType = accType
        self.profile = {}

        self.skills = [
            "Overall",
            "Attack",
            "Defence",
            "Strength",
            "Hitpoints",
            "Ranged",
            "Prayer",
            "Magic",
            "Cooking",
            "Woodcutting",
            "Fletching",
            "Fishing",
            "Firemaking",
            "Crafting",
            "Smithing",
            "Mining",
            "Herblore",
            "Agility",
            "Thieving",
            "Slayer",
            "Farming",
            "Runecrafting",
            "Hunter",
            "Construction"
            ]

        self.hiscore_apis = {
            "overall": "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=",
            "ironman": "https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player=",
            "ultimate": "https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player=",
            "hardcore": "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player="
        }

    def _parseHiscores(self, raw):
        try:
            self.data = [i.split(',') for i in raw.split('\n')]
            for n,i in enumerate(self.data[0:24]):
                self.profile[self.skills[n]] = {'rank':self.data[n][0], 'level':self.data[n][1], 'exp':self.data[n][2]}
            return True
        except:
            return False

    def lookup_player(self):
        req = requests.get(self.hiscore_apis[self.accType]+self.user)
        self._parseHiscores(req.text)

# Startup
@client.event
async def on_ready():
	print("\nTest Bot v" + botversion)
	print("\nClient logged in as:")
	print(client.user.name)
	print(client.user.id)
	print('------------------')
	time.sleep(2)
	await client.change_presence(activity=discord.Activity(name='Chilling in Falador'))

# Lookup
@client.command()
async def lookup(ctx, rsn, accountType="overall"):
    print(F"[*] Stat Lookup - {rsn}")
    hs = osrsHiScores(rsn, accountType)
    hs.lookup_player()
    embed=discord.Embed()

    embed=discord.Embed(title=F"{rsn} Stats", description="", color=0x2320fe)
    embed.set_author(name="Botonix", url="https://osrs.game/", icon_url="https://www.runescape.com/img/rsp777/social-share.jpg?1")
    embed.set_thumbnail(url="https://www.runescape.com/img/rsp777/social-share.jpg?1")

    embed.add_field(name=F"{client.get_emoji(806515209022865439)} Attack", value=hs.profile['Attack']['level'], inline=True)
    #...

    await ctx.send(embed=embed)

# Test
@client.command()
async def test(ctx, txt):
    for emoji in ctx.guild.emojis:
        print(str(emoji.id) + ' ' + str(emoji.name))

client.run(token)