from __future__ import annotations

from deck import Card, Number, Skip, Reverse, DrawTwo, Wild, DrawFourWild

import discord
from discord import app_commands
from discord.ext import commands

from models.game_state import GameState, GameError, Phase
from repos.lobby_repo import LobbyRepository
from services.lobby_service import LobbyService
from views.lobby_views import LobbyViews


def mention(user_id: int) -> str:
    return f"<@{user_id}>"


def require_channel_id(interaction: discord.Interaction) -> int:
    cid = interaction.channel_id
    if cid is None:
        raise RuntimeError("This command must be used in a server channel (not DMs).")
    return cid


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
        self.bot = bot
        self.lobby_views = LobbyViews()
        self.lobby_repo = LobbyRepository()
        self.lobby_service = LobbyService(self.lobby_repo)

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

        view = discord.ui.View(timeout=None)

        join_btn = discord.ui.Button(label="🌟 Join", style=discord.ButtonStyle.blurple)
        leave_btn = discord.ui.Button(label="🚫 Leave", style=discord.ButtonStyle.gray)
        start_btn = discord.ui.Button(label="🚀 Start Game", style=discord.ButtonStyle.success)
        cancel_btn = discord.ui.Button(label="🚨 Disband Game", style=discord.ButtonStyle.danger)

        join_btn.callback = self.join
        start_btn.callback = self.start
        leave_btn.callback = self.leave
        cancel_btn.callback = self.disband
        view.add_item(join_btn)
        view.add_item(leave_btn)
        view.add_item(start_btn)
        view.add_item(cancel_btn)

        embed = self.lobby_views.lobby_embed(lobby)
        await interaction.response.send_message(embeds=[embed], view=view)

    async def join(self, interaction: discord.Interaction) -> None:
        cid = require_channel_id(interaction)

        try:
            self.lobby_service.join_lobby(cid, interaction.user)
        except GameError as e:
            embed = self.lobby_views.error_embed("Game Join" if e.title == "" else e.title, str(e))
            await interaction.response.send_message(
                embeds=[embed],
                ephemeral=e.private,
            )
            return

        update_embed = self.lobby_views.update_embed("User Joined", f"{mention(interaction.user.id)} joined the lobby.")
        await interaction.response.send_message(
            embeds=[update_embed],
        )

    async def leave(self, interaction: discord.Interaction) -> None:
        cid = require_channel_id(interaction)

        try:
            self.lobby_service.leave_lobby(cid, interaction.user)
        except GameError as e:
            embed = self.lobby_views.error_embed("Leave" if e.title == "" else e.title, str(e), True)
            await interaction.response.send_message(
                embeds=[embed],
                ephemeral=e.private,
            )
            return

        leave_embed = self.lobby_views.update_embed(f"User Left", f"{mention(interaction.user.id)} left the lobby.")
        await interaction.response.send_message(embeds=[leave_embed])

    async def disband(self, interaction: discord.Interaction) -> None:
        cid = require_channel_id(interaction)

        try:
            self.lobby_service.disband_lobby(cid, interaction.user)
        except GameError as e:
            embed = self.lobby_views.error_embed("Must Be Host" if e.title == "" else e.title, str(e))
            await interaction.response.send_message(embeds=[embed], ephemeral=e.private)
            return

        embed = self.lobby_views.update_embed("Game Disbanded",
                                              "The host disbanded the game, so the lobby was deleted.")
        await interaction.response.send_message(embeds=[embed])

    async def start(selfself, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("this command is a work in progress")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnoCog(bot))
