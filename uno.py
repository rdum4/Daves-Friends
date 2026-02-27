"""
A Discord bot that lets you play Uno!
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
# message_content not needed for slash commands, but harmless:
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready() -> None:
    """
    When Discord is ready for the game, we set it up.
    """
    # Load lobby commands from lobby_views.py (extension style: async def setup(bot))

    ext = "controllers.uno_cog"
    if ext not in bot.extensions:
        await bot.load_extension(ext)

    # Fast sync: set GUILD_ID in .env to sync instantly in that server
    guild_id = os.getenv("GUILD_ID")
    if guild_id:
        guild = discord.Object(id=int(guild_id))
        await bot.tree.sync(guild=guild)
        print(f"Synced commands to guild {guild_id} as {bot.user}")
    else:
        # Global sync can take a while to propagate
        await bot.tree.sync()
        print(f"Synced commands globally as {bot.user}")


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("DISCORD_TOKEN is not set. Check your .env file.")

bot.run(token)
