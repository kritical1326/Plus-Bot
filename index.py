import discord
import os
import requests
import json
from keep_alive import keep_alive
import asyncio


client = discord.Client()

def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + json_data['punchline']
  return(joke)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
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

keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
