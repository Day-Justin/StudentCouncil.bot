# A moderate moderation Bot


import discord
from discord.ext import commands
import os
import random
import logging
import json
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TOKEN")


with open('../config.json') as f:
    data = json.load(f)
    PREFIX = data["StudentCouncil"]["PREFIX"]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
logger.addHandler(handler)


client = discord.Client()
bot = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


welcome_channel = 1017123907658076252
@client.event
async def on_member_join(member):
    member.guild.channels.get_channel(welcome_channel).send(f'<@{member.id}>Welcome to the server!')


# Start each command with the @bot.command decorater
@bot.command()
async def info(ctx):
    """
    ctx - context
    (prefix)info
    """
    await ctx.send (ctx.guild)
    await ctx.send (ctx.author)
    await ctx.send (ctx.message.id)


@bot.command()
async def square(ctx, arg):  # The name of the function is the name of the command
    print(arg)  # this is the text that follows the command
    await ctx.send(int(arg) ** 2)  # ctx.send sends text in chat


def get_quote():
    response = request.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote





client.run(TOKEN)
bot.run(TOKEN)

