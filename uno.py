import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def ping(ctx: commands.Context[commands.Bot], arg: str = ""):
    await ctx.send(f"pong {arg}")

token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise RuntimeError("DISCORD_TOKEN is not set in .env")

bot.run(token)
