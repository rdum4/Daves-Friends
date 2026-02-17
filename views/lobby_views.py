import discord
from discord import Colour

from models.lobby_model import Lobby
from views.base_views import BaseViews


class LobbyViews(BaseViews):
    def lobby_embed(self, lobby: Lobby) -> discord.Embed:
        return self._build_embed(title="New Uno Lobby Open By " + lobby.user.name,
                                 desc="A new uno lobby is being hosted by <@" + str(
                                     lobby.user.id) + ">. To join, click the `🌟 Join` button.",
                                 color=self.get_random_color(), gif=True, footer=True, time_stamp=True,
                                 random_gif=True, author=lobby.user)
