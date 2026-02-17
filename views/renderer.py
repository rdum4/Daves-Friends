import discord

from models.game_state import Phase
from models.lobby_model import Lobby
from services.game_service import GameService
from services.lobby_service import LobbyService
from views.game_views import GameViews
from views.lobby_views import LobbyViews
from UI.lobby_ui import LobbyUI
from UI.interactions import Interactions

class Renderer:
    # my python is rusty but im pretty sure all this is passed in as reference?
    def __init__(self, lobby_views: LobbyViews, game_views: GameViews, lobby_service: LobbyService,
                 game_service: GameService):
        self.lobby_views = lobby_views
        self.game_views = game_views
        self.lobby_service = lobby_service

    async def render(self, lobby: Lobby) -> (list[discord.Embed], Interactions):
        if lobby.game.phase() == Phase.LOBBY:
            embed = self.lobby_views.lobby_embed(lobby)
            views = LobbyUI(self, self.lobby_service, self.lobby_views)

            return [embed], views
        else:
            pass
            # embed = self.game_views

    async def update_from_interaction(self, interaction: discord.Interaction, lobby: Lobby):
        embeds, view = await self.render(lobby)

        if not interaction.response.is_done():
            await interaction.response.edit_message(embeds=embeds, view=view)
        else:
            await interaction.message.edit(embeds=embeds, view=view)

    async def update_by_message_id(self, bot: discord.Client, channel_id: int, message_id: int, lobby: Lobby):
        pass