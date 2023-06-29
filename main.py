import requests, discord, json
from discord import app_commands 
from bs4 import BeautifulSoup
from datetime import datetime

with open("config.json", encoding='utf-8') as config:
    read_config = json.load(config)
    token = read_config['token']

current_id = 'mw-customcollapsible-current' #id do element div (current stock)
last_id = 'mw-customcollapsible-last' #id do elemento div (last stock)
before_last_id = 'mw-customcollapsible-beforelast' #id do element div (before last stock)

fruits = {  "kilo":"<:kilo:1109562877746102292>    **Kilo** - $ 5.000 - <:robux:1123951146659225641> 50\n",
            "spin":"<:spin:1109562889066532885>    **Spin** - $ 7.500 - <:robux:1123951146659225641> 75\n",
            "chop":"<:chop:1109562863124742164>    **Chop** - $ 30.000 - <:robux:1123951146659225641> 100\n",
            "spring":"<:spring:1109562890932985958>    **Spring** - $ 60.000 - <:robux:1123951146659225641> 180\n",
            "bomb":"<:bomb_fruit:1109562860767551529>    **Bomb** - $ 80.000 - <:robux:1123951146659225641> 220\n",
            "smoke":"<:smoke:1109565821782597782>    **Smoke** - $ 100.000 - <:robux:1123951146659225641> 250\n",
            "spike":"<:spike:1109540994975797269>    **Spike** - $ 180.000 - <:robux:1123951146659225641> 380\n",
            "flame":"<:flame_fruit:1109562870880014426>    **Flame** - $ 250.000 - <:robux:1123951146659225641> 550\n",
            "falcon":"<:falcon:1109562867742687305>    **Falcon** - $ 300.000 - <:robux:1123951146659225641> 650\n",
            "ice":"<:ice:1109562875938353182>    **Ice** - $ 350.000 - <:robux:1123951146659225641> 750\n",
            "sand":"<:sand:1109562884335341618>    **Sand** - $ 420.000 - <:robux:1123951146659225641> 850\n",
            "dark":"<:dark:1109562865813307463>    **Dark** - $ 500.000 - <:robux:1123951146659225641> 950\n",
            "revive":"<:revive:1109562881369968703>    **Revive** - $ 550.000 - <:robux:1123951146659225641> 975\n",
            ":diamond":"<:diamond:1109541792346546206>    **Diamond** - $ 600.000 - <:robux:1123951146659225641> 1.000\n",
            "light":"<:light:1109541790744313866>    **Light** - $ 650.000 - <:robux:1123951146659225641> 1.100\n",
            "rubber":"<:rubber:1109541787825086525>    **Rubber** - $ 750.000 - <:robux:1123951146659225641> 1.200\n",
            "barrier":"<:barrier:1109541004551405700>    **Barrier** - $ 800.000 - <:robux:1123951146659225641> 1.250\n",
            "magma":"<:magma:1109541007814570045>    **Magma** - $ 850.000 - <:robux:1123951146659225641> 1.300\n",
            "quake":"<:quake:1109540999711170631>    **Quake** - $ 1,000.000 - <:robux:1123951146659225641> 1.500\n",
            "buddha":"<:buddha:1109540997903437964>    **Buddha** - $ 1.200,000 - <:robux:1123951146659225641> 1.650\n",
            "love":"<:love:1109541010985463818>    **Love** - $ 1.300,000 - <:robux:1123951146659225641> 1.700\n",
            "spider":"<:spider_fruit:1109562886226968576>    **Spider** - $ 1.500,000 - <:robux:1123951146659225641> 1.800\n",
            "phoenix":"<:phoenix:1109540993486827550>    **Phoenix** - $ 1.800,000 - <:robux:1123951146659225641> 2.000\n",
            "portal":"<:portal:1109541002785591417>    **Portal** - $ 1.900,000 - <:robux:1123951146659225641> 2.000\n",
            "rumble":"<:rumble:1109540990735360042>    **Rumble** - $ 2.100,000 - <:robux:1123951146659225641> 2.100\n",
            "paw":"<:paw:1109540989099577554>    **Paw** - $ 2.300,000 - <:robux:1123951146659225641> 2.200\n",
            "blizzard":"<:blizzard:1109540986167758898>    **Blizzard** - $ 2.400,000 - <:robux:1123951146659225641> 2.250\n",
            "gravity":"<:gravity:1109541050059608174>    **Gravity** - $ 2.500,000 - <:robux:1123951146659225641> 2.300\n",
            "dough":"<:dough:1109541017415336036>    **Dough** - $ 2.800,000 - <:robux:1123951146659225641> 2.400\n",
            "shadow":"<:shadow:1109541020607189104>    **Shadow** - $ 2.900,000 - <:robux:1123951146659225641> 2.425\n",
            "venom":"<:venom:1109541022561747026>    **Venom** - $ 3.000,000 - <:robux:1123951146659225641> 2.450\n",
            "control":"<:control:1109541025447424144>    **Control** - $ 3.200,000 - <:robux:1123951146659225641> 2.500\n",
            "spirit":"<:spirit:1109541795395817602>    **Spirit** - $ 3.400,000 - <:robux:1123951146659225641> 2.550\n",
            "dragon":"<:dragon_fruit:1109541030610604144>    **Dragon** - $ 3.500,000 - <:robux:1123951146659225641> 2.600\n",
            "leopard":"<:leopard_fruit:1109541033898954892>    **Leopard** - $ 5.000,000 - <:robux:1123951146659225641> 3.000\n" 
            }

def format_fruit(x):
    site = requests.get('https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22').text
    soup = BeautifulSoup(site, 'html.parser')
    stock = []
    for f1 in soup.find_all(id=x):
        for f2 in f1.find_all('figure'):
            for f3 in f2.find_all('a'):
                for f4 in f3.find_all('span'):
                    stock.append(f4.string.lower())
    return stock

def func_h():

    reset1 = 10000
    reset2 = 50000
    reset3 = 90000
    reset4 = 130000
    reset5 = 170000
    reset6 = 210000

    fhora = int(datetime.today().strftime('%H%M%S'))
    
    h = int(datetime.today().strftime('%H'))
    m = int(datetime.today().strftime('%M'))
    s = int(datetime.today().strftime('%S'))

    h = h + 1
    m = (59 - m)
    s = (60 - s)

    if fhora >= reset1 and fhora < reset2:
        h = (5 - h)
    elif fhora >= reset2 and fhora < reset3:
        h = (9 - h)
    elif fhora >= reset3 and fhora < reset4:
        h = (13 - h)
    elif fhora >= reset4 and fhora < reset5:
        h = (17 - h)
    elif fhora >= reset5 and fhora < reset6:
        h = (21 - h)
    elif fhora >= reset6:
        h = (24 - h)  
    elif fhora < reset1:
        h = (1 - h)  

    hora_stock = '{}H {}M {}S'.format(h, m, s)

    return hora_stock

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False 

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync()
            self.synced = True
        print(f"- BOT [online] - Logado como {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = 'stock', description = 'Estoque do vendedor de frutas')
async def towers(interaction):
    current_stock = format_fruit(current_id)
    last_stock = format_fruit(last_id)

    current_stock_f = ''
    for csf in current_stock:
        current_stock_f = current_stock_f + fruits[csf]

    last_stock_f = ''
    for lsf in last_stock:
        last_stock_f = last_stock_f + fruits[lsf]

    #

    em = discord.Embed(colour=0x0025ff, color=0x0025ff, title='Blox Fruits "Stock"', type='rich', url=None, description='Estoque do Blox Fruit Dealer', timestamp=None)
    #em.set_author(name='LeoSzinTV', url=None, icon_url='https://media.discordapp.net/attachments/1120403497591001138/1120403721550057563/logo.png')
    em.add_field(name=f'Estoque atual  `{func_h()}`', value="{}".format(current_stock_f), inline=False)
    em.add_field(name='Último estoque', value=f"{last_stock_f}", inline=False)
    #em.set_image(url='https://static.wikia.nocookie.net/roblox-blox-piece/images/5/50/Flame.GIF/revision/latest?cb=20220919063135')
    em.set_footer(text='© LeoSzinTV Community - Todos os direitos reservados', icon_url=None)

    await interaction.response.send_message(embed=em)


client.run(token)