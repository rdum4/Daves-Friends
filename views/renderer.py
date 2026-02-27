"""
Provides a renderer for all of the views.
"""

import discord

from ui.end_ui import EndUI
from ui.game_ui import GameUI
from ui.lobby_ui import LobbyUI
from ui.interactions import Interactions
from models.game_state import Phase
from models.lobby_model import Lobby
from services.game_service import GameService
from services.lobby_service import LobbyService
from views.end_views import EndViews
from views.game_views import GameViews
from views.hand_views import HandViews
from views.lobby_views import LobbyViews


class Renderer:
    """
    The renderer which compiles and manages all of the views.
    """

    def __init__(
        self,
        lobby_service: LobbyService,
        game_service: GameService,
    ):
        self.lobby_views = LobbyViews()
        self.game_views = GameViews()
        self.end_views = EndViews()
        self.hand_views = HandViews()

        self.lobby_service = lobby_service
        self.game_service = game_service

    async def render(
        self, lobby: Lobby
    ) -> tuple[list[discord.Embed], Interactions, list[discord.File]]:
        """
        Renders all of the views to a list of embeds.
        """

        if lobby.game.phase() == Phase.LOBBY:
            embed = self.lobby_views.lobby_embed(lobby)
            views = LobbyUI(self, self.lobby_service, self.lobby_views)
            return [embed], views, []

        if lobby.game.phase() == Phase.PLAYING:
            embed, file = self.game_views.game_embed(lobby)
            views = GameUI(self, lobby, self.game_service)
            return [embed], views, [file] if file else []

        if lobby.game.phase() == Phase.FINISHED:
            embed = self.end_views.end_embed(lobby)
            views = EndUI()
            return [embed], views, []

        raise RuntimeError("Unknown phase")

    async def update_from_interaction(
        self, interaction: discord.Interaction, lobby: Lobby
    ):
        """
        Updates a view based on a Discord interaction.
        """

        embeds, view, files = await self.render(lobby)

        if not interaction.response.is_done():
            await interaction.response.edit_message(
                embeds=embeds,
                view=view,
                attachments=files,
            )
        else:
            assert interaction.message is not None
            await interaction.message.edit(
                embeds=embeds,
                view=view,
                attachments=files,
            )

    async def update_by_message_id(
        self,
        bot: discord.Client,
        channel_id: int,
        message_id: int,
        lobby: Lobby,
    ):
        """
        Re-renders an embed by its message ID.
        """

        embeds, view, files = await self.render(lobby)

        channel = bot.get_channel(channel_id)
        if channel is None:
            channel = await bot.fetch_channel(channel_id)

        message = await channel.fetch_message(message_id)

        await message.edit(
            embeds=embeds,
            view=view,
            attachments=files,
        )
