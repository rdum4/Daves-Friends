import discord
from models.lobby_model import Lobby
from utils.utils import mention
from views.base_views import BaseViews


class LobbyViews(BaseViews):
    def lobby_embed(self, lobby: Lobby) -> discord.Embed:
        embed = self._build_embed(title="New Uno Lobby Open By " + lobby.user.name,
                                 desc="A new uno lobby is being hosted by <@" + str(
                                     lobby.user.id) + ">. To join, click the `🌟 Join` button.",
                                 color=self.get_random_color(), gif=True, footer=True, time_stamp=True,
                                 random_gif=True, author=lobby.user)

        users_str = mention(lobby.user.id) + "(Host)"

        for player in lobby.game.players():
            if player == lobby.user.id:
                continue
            users_str += "\n" + mention(player)

        embed.add_field(name="Users In Lobby", value=users_str, inline=False)

        return embed