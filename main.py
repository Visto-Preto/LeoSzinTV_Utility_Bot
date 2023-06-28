import requests, discord, json
from discord import app_commands 
from bs4 import BeautifulSoup

with open("config.json", encoding='utf-8') as config:
    read_config = json.load(config)
    token = read_config['token']

current_id = 'mw-customcollapsible-current' #id do element div (current stock)
last_id = 'mw-customcollapsible-last' #id do elemento div (last stock)
before_last_id = 'mw-customcollapsible-beforelast' #id do element div (before last stock)

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

@tree.command(name = 'stock', description='Estoque do vendedor de frutas')
async def towers(interaction):
    current_stock = format_fruit(current_id)
    last_stock = format_fruit(last_id)
    
    #https://media.discordapp.net/attachments/1120403497591001138/1120403721550057563/logo.png
    em = discord.Embed(colour=0x0025ff, color=0x0025ff, title='Blox Fruits "Stock', type='rich', url=None, description='Estoque de frutas do vendedor de frutas do Blox Fruits', timestamp=None)
    em.add_field(name='Estoque atual `1H 50H 20S`', value=f"{current_stock}", inline=False)
    em.add_field(name='Último estoque', value=f"{last_stock}", inline=False)
    em.set_footer(text='© LeoSzinTV Community - Todos os direitos reservados', icon_url=None)
    await interaction.response.send_message(embed=em)



client.run(token)