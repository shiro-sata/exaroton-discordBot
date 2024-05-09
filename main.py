import discord
import asyncio
from exaroton import Exaroton

TOKEN = '--> Your discord token here <--'
SERVER_ID = 'Server ID of your EXAROTON server'
EXAROTON_API_TOKEN = '-->your EXAROTON API token here <--'
CHANNEL_ID = Channe ID of your discord server

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

exaroton = Exaroton(EXAROTON_API_TOKEN)

previous_status = None
previous_players = []

async def check_server_status():
    global previous_status, previous_players
    await client.wait_until_ready()
    while not client.is_closed():
        server = exaroton.get_server(SERVER_ID)
        if server.status == 'Online':
            current_status = "✅ Server Online"
        else:
            current_status = "⛔️ Server Closed"
        if current_status != previous_status:
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(current_status)
            previous_status = current_status
        
        players = server.players.list
        if players != previous_players:
            for player in players:
                if player not in previous_players:
                    await channel.send(f"➕***{player}*** joined the server.")
            
            for player in previous_players:
                if player not in players:
                    await channel.send(f"➖***{player}*** left the server.")
            
            previous_players = players
        
        await asyncio.sleep(3)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')
    client.loop.create_task(check_server_status())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    server = exaroton.get_server(SERVER_ID)
    if message.content.startswith("!stats"):
        if server.status == 'Online':
            current_status = "✅ Server Online"
        else:
            current_status = "⛔️ Server Closed"
        await message.channel.send(current_status + "\n\n🎯***Player Info***🎯\n- Player connected : " + str(server.players.count) + "\n- List of players :" + str(server.players.list) + "\n\n***Account***\ncredit left : ***" +str(exaroton.get_account().credits)+ "***")
client.run(TOKEN)
