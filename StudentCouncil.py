# A moderate moderation Bot

import discord
from discord.ext import commands
import os
import random
import logging
import json


with open(os.path.dirname(__file__) + '/../config.json') as f:
    data = json.load(f)
    TOKEN = data["StudentCouncil"]["TOKEN"]
    prefix = data["StudentCouncil"]["PREFIX"]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
logger.addHandler(handler)


intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


welcome_channel = 1017123907658076252
@bot.event
async def on_member_join(member):
    member.guild.channels.get_channel(welcome_channel).send(f'<@{member.id}>Welcome to the server!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')
    if message.content == 'bye':
        await message.channel.send(f'Goodbye {message.author}')

    await bot.process_commands(message)


# Start each command with the @bot.command decorater
@bot.command()
async def square(ctx, arg):  # The name of the function is the name of the command
    print(arg)  # this is the text that follows the command
    await ctx.send(int(arg) ** 2)  # ctx.send sends text in chat


bot.run(TOKEN)

