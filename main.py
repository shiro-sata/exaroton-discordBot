import discord
import asyncio
from exaroton import Exaroton

# Token de votre bot Discord
TOKEN = 'MTIzNzE1NTczMTg3NTA0MTMwMQ.GnLAdp.0QWsbGukhtSGZ2_3eAzU58H8osYLvjsuCOH990'

# ID de votre serveur exaroton
SERVER_ID = 'BjTyWMoJoMfs6ZhO'

# Token API de exaroton
EXAROTON_API_TOKEN = 'VOjFiM46X9M8LsiUJoWOsjyigzMzuu8kQCKsGqv4EQ6c8Xdgz3DKPBkSsGyaOnoPookmf3DALGQ9N4PHaA4JeeDu9RH5ldZoEzRp'

# ID du canal Discord où envoyer les messages
CHANNEL_ID = 1237142631444643871

# Initialisation du client Discord avec les intentions
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

# Initialisation de la connexion exaroton avec le token API
exaroton = Exaroton(EXAROTON_API_TOKEN)

# Store previous state of the server and players
previous_status = None
previous_players = []

async def check_server_status():
    global previous_status, previous_players
    await client.wait_until_ready()
    while not client.is_closed():
        # Obtenir l'objet Server exaroton
        server = exaroton.get_server(SERVER_ID)
        
        # Vérifier si le serveur est en ligne ou hors ligne
        if server.status == 'Online':
            current_status = "✅ Server Online"
        else:
            current_status = "⛔️ Server Closed"
        
        # Envoyer le message seulement si le statut a changé
        if current_status != previous_status:
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(current_status)
            previous_status = current_status
        
        # Obtenir la liste des joueurs actuellement connectés
        players = server.players.list
        
        # Vérifier si la liste des joueurs a changé
        if players != previous_players:
            for player in players:
                # Vérifier si le joueur vient de se connecter
                if player not in previous_players:
                    # Envoyer un message pour informer qu'un joueur s'est connecté
                    await channel.send(f"➕***{player}*** joined the server.")
            
            for player in previous_players:
                # Vérifier si le joueur a quitté le serveur
                if player not in players:
                    # Envoyer un message pour informer qu'un joueur s'est déconnecté
                    await channel.send(f"➖***{player}*** left the server.")
            
            previous_players = players
        
        # Attendre 15 secondes avant de vérifier à nouveau
        await asyncio.sleep(3)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')
    # Démarrer la vérification de l'état du serveur
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
