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

fruits = {  "kilo":":kilo:    Kilo - $ 5.000 - :robux: 50\n",
            "spin":":spin:    Spin - $ 7.500 - :robux: 75\n",
            "chop":":chop:    Chop - $ 30.000 - :robux: 100\n",
            "spring":":spring:    Spring - $ 60.000 - :robux: 180\n",
            "bomb":":bomb_fruit:    Bomb - $ 80.000 - :robux: 220\n",
            "smoke":":smoke:    Smoke - $ 100.000 - :robux: 250\n",
            "spike":":spike:    Spike - $ 180.000 - :robux: 380\n",
            "flame":":flame_fruit:    Flame - $ 250.000 - :robux: 550\n",
            "falcon":":falcon:    Falcon - $ 300.000 - :robux: 650\n",
            "ice":":ice:    Ice - $ 350.000 - :robux: 750\n",
            "sand":":sand:    Sand - $ 420.000 - :robux: 850\n",
            "dark":":dark:    Dark - $ 500.000 - :robux: 950\n",
            "revive":":revive:    Revive - $ 550.000 - :robux: 975\n",
            ":diamond":":diamond:    Diamond - $ 600.000 - :robux: 1,000\n",
            "light":":light:    Light - $ 650.000 - :robux: 1,100\n",
            "rubber":":rubber:    Rubber - $ 750.000 - :robux: 1,200\n",
            "barrier":":barrier:    Barrier - $ 800.000:robux: 1,250\n",
            "magma":":magma:    Magma - $ 850.000 - :robux: 1,300\n",
            "quake":":quake:    Quake - $ 1,000.000 - :robux: 1,500\n",
            "buddha":":buddha:    Buddha - $ 1.200,000 - :robux: 1,650\n",
            "love":":love:    Love - $ 1.300,000 - :robux: 1,700\n",
            "spider":":spider_fruit:    Spider - $ 1.500,000 - :robux: 1,800\n",
            "phoenix":":phoenix:    Phoenix - $ 1.800,000 - :robux: 2,000\n",
            "portal":":portal:    Portal - $ 1.900,000 - :robux: 2,000\n",
            "rumble":":rumble:    Rumble - $ 2.100,000 - :robux: 2,100\n",
            "paw":":paw:    Paw - $ 2.300,000 - :robux: 2,200\n",
            "blizzard":":blizzard:    Blizzard - $ 2.400,000 - :robux: 2,250\n",
            "gravity":":gravity:    Gravity - $ 2.500,000 - :robux: 2,300\n",
            "dough":":dough:    Dough - $ 2.800,000 - :robux: 2,400\n",
            "shadow":":shadow:    Shadow - $ 2.900,000 - :robux: 2,425\n",
            "venom":":venom:    Venom - $ 3.000,000 - :robux: 2,450\n",
            "control":":control:    Control - $ 3.200,000 - :robux: 2,500\n",
            "spirit":":spirit:    Spirit - $ 3.400,000 - :robux: 2,550\n",
            "dragon":":dragon_fruit:    Dragon - $ 3.500,000 - :robux: 2,600\n",
            "leopard":":leopard_fruit:    Leopard - $ 5.000,000 - :robux: 3,000\n" 
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

    #https://media.discordapp.net/attachments/1120403497591001138/1120403721550057563/logo.png
    em = discord.Embed(colour=0x0025ff, color=0x0025ff, title='Blox Fruits "Stock"', type='rich', url=None, description='Estoque do Blox Fruit Dealer', timestamp=None)
    em.add_field(name=f'Estoque atual  `{func_h()}`', value="{}".format(current_stock_f), inline=False)
    em.add_field(name='Último estoque', value=f"{last_stock_f}", inline=False)
    em.set_footer(text='© LeoSzinTV Community - Todos os direitos reservados', icon_url=None)
    await interaction.response.send_message(embed=em)

client.run(token)