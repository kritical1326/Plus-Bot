import discord
import os
import requests
import json
from keep_alive import keep_alive
import asyncio
import random
from discord.ext import commands
from replit import db

client = discord.Client()

sad_words = [
    "sad", "depressed", "depressing", "hopeless", "i'm feeling low", "unhappy",
    "angry", "frustrated", "miserable", "I'm feeling low", "im feeling low"
]

encouragement = [
    "Hang in there. Here's a joke for you!",
    "You got this. Here's a joke for you!",
    "I hope you feel better. Here's a joke for you!",
    "Cheer up! Better things will come your way. Like this joke -",
    "You're a great person! Here's a joke for you."
]

if "responding" not in db.keys():
    db["responding"] = True


def get_joke():
    response = requests.get(
        "https://official-joke-api.appspot.com/random_joke")
    json_data = json.loads(response.text)
    joke = json_data['setup'] + json_data['punchline']
    return (joke)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('With Words'))


@client.event
async def on_guild_join(guild):
    channel = await guild.create_text_channel('plus-bot')
    await channel.send("Make way for me. I'm here!")

channels = ['plus-bot']

@client.event
async def on_message(message):
    if str(message.channel) in channels:
        if message.author == client.user:
            return

        if message.content.startswith('+hello'):
            await message.channel.send('Hello!')

        if message.content.startswith('+joke'):
            joke = get_joke()
            await message.channel.send(joke)

        if message.content.startswith('+forever'):

            async def hello():
                joke = get_joke()
                await message.channel.send(joke)
                await asyncio.sleep(3600)
                await hello()

            await hello()

        msg = message.content

        if db["responding"]:
            if any(word in msg for word in sad_words):
                await message.channel.send(random.choice(encouragement))
                joke = get_joke()
                await message.channel.send(joke)


keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
