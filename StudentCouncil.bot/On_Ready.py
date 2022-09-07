import nextcord
from nextcord.ext import commands
import os
import json
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = nextcord.Intents.default()
intents.message_content = True


with open('../config.json') as f:
    data = json.load(f)
    PREFIX = data["StudentCouncil"]["PREFIX"]


client = commands.Bot(command_prefix=PREFIX, intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.command()
async def info(ctx):
    """
    ctx - context
    (prefix)info
    """
    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)
    await ctx.send(ctx.channel)


client.run(TOKEN)