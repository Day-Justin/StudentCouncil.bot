import nextcord
from nextcord.ext import commands
import os
import json
from dotenv import load_dotenv
import logging


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = nextcord.Intents.default()
intents.message_content = True


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
# logger.addHandler(handler)



with open('../config.json') as f:
    data = json.load(f)
    PREFIX = data["StudentCouncil"]["PREFIX"]


client = commands.Bot(command_prefix=PREFIX, intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(TOKEN)