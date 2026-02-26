from __future__ import annotations
from UI.interactions import Interactions
import discord

from models.game_state import GameError, Phase
from models.lobby_model import Lobby
from services.game_service import GameService
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.renderer import Renderer



class GameUI(Interactions):
    def __init__(self, renderer: Renderer, lobby: Lobby, game_service: GameService):
        super().__init__()
        self._renderer = renderer
        self.lobby: Lobby = lobby
        self.game_service: GameService = game_service

    @discord.ui.button(label="1️⃣ Call Uno", style=discord.ButtonStyle.success)
    async def call_uno(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("this command is a work in progress")

    @discord.ui.button(label="👀 View Cards", style=discord.ButtonStyle.blurple)
    async def view_cards(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        user_id = interaction.user.id
        game = self.lobby.game

        if game.phase() != Phase.PLAYING:
            await interaction.response.send_message("Game is not currently active.", ephemeral=True)
            return

        hand = game.hand(user_id)

        if not hand:
            await interaction.response.send_message("You are not in this game.", ephemeral=True)
            return

        embed = self._renderer.hand_views.hand_embed(hand)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🃏 Draw Card and Pass", style=discord.ButtonStyle.gray)
    async def draw_card_and_pass(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        try:
            self.game_service.draw(interaction.channel_id, interaction.user.id)

        except GameError as e:
            embed = self._renderer.lobby_views.error_embed("Not your turn!" if e.title == "" else e.title, str(e))
            await interaction.response.send_message(embeds=[embed], ephemeral=e.private)

            return

        await self._renderer.update_from_interaction(interaction, self.lobby)