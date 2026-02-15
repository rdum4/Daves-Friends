import discord
from discord import Colour

from models.lobby_model import Lobby
from views.base_views import BaseViews


class LobbyViews(BaseViews):
    def lobby_embed(self, lobby: Lobby):
        embed = discord.Embed(
            title="New Uno Lobby Open By " + lobby.user.name,
            description="A new uno lobby is being hosted by <@" + str(
                lobby.user.id) + ">. To join, use the `/join` command.",
            colour=self.get_random_color(),
        )

        embed.set_author(name=lobby.user.name, icon_url=lobby.user.avatar.url)
        embed.set_image(url=self.get_random_gif())

        embed.set_footer(text="Uno Discord Bot • Class Project for UWB 360")
        embed.timestamp = discord.utils.utcnow()

        return embed
