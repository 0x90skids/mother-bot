import discord
import asyncio
import os
import talk
from keep_alive import keep_alive

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
client = discord.Client()

@client.event
async def on_ready():
  print("Bot running...".format(client))
  channel = client.get_channel(CHANNEL_ID)
  # replit randomly reboots causing spam
  #await channel.send(file=discord.File('mother.jpeg'))
  while True:
    await asyncio.sleep(60)
    trigger = talk.notify()
    if trigger:
      await channel.send(trigger)
@client.event
async def on_message(message):
  if (message.author != client.user) or not (message.channel.id == CHANNEL_ID):
    if message.content.startswith('$'):
      await message.channel.send(talk.answer(*message.content[1:].split()))

keep_alive()
client.run(BOT_TOKEN)