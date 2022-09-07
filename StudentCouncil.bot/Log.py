import nextcord
from nextcord.ext import commands
import os
import json
from dotenv import load_dotenv
import logging


logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = nextcord.Intents.default()
intents.message_content = True


with open('../config.json') as f:
    data = json.load(f)
    PREFIX = data["StudentCouncil"]["PREFIX"]


client = commands.Bot(command_prefix=PREFIX, intents=intents)
bot_channel = 797357086236213258


@client.event
async def on_ready():
    print(f'Log is ready')


@client.event
async def on_message_edit(before, after):
    await before.channel.send(
        f'{before.author} edited a message.\n'
        f' Before: {before.content}\n'
        f'After: {after.content}\n'
    )


client.run(TOKEN)