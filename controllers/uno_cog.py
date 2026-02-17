from __future__ import annotations

from deck import Card, Number, Skip, Reverse, DrawTwo, Wild, DrawFourWild

import discord
from discord import app_commands
from discord.ext import commands

from models.game_state import GameState, GameError, Phase
from repos.lobby_repo import LobbyRepository
from services.game_service import GameService
from services.lobby_service import LobbyService
from utils.utils import require_channel_id
from views.game_views import GameViews
from views.lobby_views import LobbyViews
from views.renderer import Renderer


def format_card(card: Card | None) -> str:
    if card is None:
        return "(none)"
    if isinstance(card, Number):
        return f"{card.color.name} {card.number}"
    if isinstance(card, Skip):
        return f"{card.color.name} SKIP"
    if isinstance(card, Reverse):
        return f"{card.color.name} REVERSE"
    if isinstance(card, DrawTwo):
        return f"{card.color.name} DRAW2"
    if isinstance(card, DrawFourWild):
        return f"DRAW4 ({card.color.name if card.color else 'unpicked'})"
    if isinstance(card, Wild):
        return f"WILD ({card.color.name if card.color else 'unpicked'})"
    return str(card)


class UnoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        # Bot
        self.bot = bot

        # Views
        self.lobby_views = LobbyViews()
        self.game_views = GameViews()

        # Repos
        self.lobby_repo = LobbyRepository()

        # Services
        self.lobby_service = LobbyService(self.lobby_repo)
        self.game_service = GameService()

        # Misc
        self._renderer = Renderer(self.lobby_views, self.game_views, self.lobby_service, self.game_service)

    @app_commands.command(name="create", description="Create a lobby in this channel.")
    async def create(self, interaction: discord.Interaction) -> None:
        cid = require_channel_id(interaction)

        try:
            lobby = self.lobby_service.create_lobby(cid, interaction.user)
        except GameError as e:
            print("In the error")

            embed = self.lobby_views.error_embed("Lobby Exists" if e.title == "" else e.title, str(e))
            await interaction.response.send_message(embeds=[embed], ephemeral=e.private)

            return

        embeds, view = await self._renderer.render(lobby)
        await interaction.response.send_message(embeds=embeds, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnoCog(bot))
