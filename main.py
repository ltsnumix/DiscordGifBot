import os
import discord
from discord.ext import commands
from PIL import Image
import imageio
import requests
from io import BytesIO
from keep_alive import keep_alive

keep_alive()

token = os.environ['TOKEN']

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='>',intents=intents)

@bot.command()
async def ping(ctx):
  await ctx.send('{0}'.format(round(bot.latency, 1)), delete_after=3)

@bot.event
async def on_message(message):
    # Check if the message is a reply to an image
    if message.reference and message.content == '>gif':
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        if len(referenced_message.attachments) > 0:
            url = referenced_message.attachments[0].url
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            # Create a GIF
            frames = [img]
            with BytesIO() as output:
                imageio.mimsave(output, frames, 'GIF', duration=0.5)
                bytes = output.getvalue()

            await message.reply(file=discord.File(BytesIO(bytes), 'image.gif'))

    # Process commands after checking for the '>gif' reply
    await bot.process_commands(message)

bot.run(token)
