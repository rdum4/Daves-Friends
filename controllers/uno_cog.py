from __future__ import annotations

import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from models.deck import Card, Number, Skip, Reverse, DrawTwo, Wild, DrawFourWild, Color
from models.game_state import GameError
from repos.lobby_repo import LobbyRepository
from services.game_service import GameService
from services.lobby_service import LobbyService
from utils.utils import require_channel_id
from views.end_views import EndViews
from views.game_views import GameViews
from views.hand_views import HandViews
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

        # Repos
        self.lobby_repo = LobbyRepository()

        # Services
        self.lobby_service = LobbyService(self.lobby_repo)
        self.game_service = GameService(self.lobby_service)

        # Initialize renderer
        self._renderer = Renderer(self.lobby_service, self.game_service)

    @app_commands.command(name="create", description="Create a lobby in this channel.")
    async def create(self, interaction: discord.Interaction) -> None:
        cid = require_channel_id(interaction)

        try:
            lobby = self.lobby_service.create_lobby(cid, interaction.user)
        except GameError as e:
            embed = self.lobby_views.error_embed(
                "Lobby Exists" if e.title == "" else e.title, str(e)
            )
            await interaction.response.send_message(embeds=[embed], ephemeral=e.private)

            return

        embeds, view, files = await self._renderer.render(lobby)
        await interaction.response.send_message(embeds=embeds, view=view, files=files)
        msg = await interaction.original_response()
        lobby.main_message = msg.id

    @app_commands.command(
        name="play",
        description="Play a card from your hand on your turn (index starts at 0).",
    )
    @app_commands.describe(
        card_index="Index of the card in your hand (0-based).",
        color="Required for Wild / Draw4 (red/yellow/blue/green).",
    )
    @app_commands.choices(
        color=[
            app_commands.Choice(name="Red", value="red"),
            app_commands.Choice(name="Yellow", value="yellow"),
            app_commands.Choice(name="Blue", value="blue"),
            app_commands.Choice(name="Green", value="green"),
        ]
    )
    async def play(
        self,
        interaction: discord.Interaction,
        card_index: int | None = None,
        color: app_commands.Choice[str] | None = None,
    ) -> None:
        cid = require_channel_id(interaction)
        lobby = self.lobby_service.get_lobby(cid)
        main_msg_id = lobby.main_message

        try:
            if card_index is None and color is None:
                raise GameError(
                    "You must specify either a card index or a color.",
                    title="Game Error",
                    private=True,
                )

            self.game_service.play_card(
                cid,
                interaction.user.id,
                card_index,
                Color[color.value.upper()] if color else None,
            )
        except GameError as e:
            embed = self.lobby_views.error_embed(
                "Lobby Exists" if e.title == "" else e.title, str(e)
            )
            await interaction.response.send_message(embeds=[embed], ephemeral=e.private)

            return

        await self._renderer.update_by_message_id(self.bot, cid, main_msg_id, lobby)
        await interaction.response.send_message(
            "Successfully played card!", ephemeral=True
        )

        bot = interaction.client
        guild = interaction.guild.id
        user = await bot.fetch_user(interaction.user.id)
        hand = lobby.game.hand(interaction.user.id)
        embed = self.hand_views.hand_embed(
            hand,
            optional_message=f"""This is your new hand after your latest action.
            Link to Game: https://discord.com/channels/{guild}/{cid}/{lobby.main_message}""",
        )

        await user.send(embed=embed)

    async def _run_afk_timer(
        self, channel_id: int, player_id: int, start_turn_count: int
    ):
        await asyncio.sleep(60)

        try:
            lobby = self.lobby_service.get_lobby(channel_id)
            game = lobby.game
        except Exception:
            return

        if game.phase().name != "PLAYING":
            return

        if (
            game.current_player() == player_id
            and game.state["turn_count"] == start_turn_count
        ):
            try:
                game.draw_and_pass(player_id)

                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(
                        f" <@{player_id}> was AFK. They drew a card and was skipped."
                    )

                    embeds, view, files = await self._renderer.render(lobby)
                    await channel.send(embeds=embeds, view=view, files=files)

                    asyncio.create_task(
                        self._run_afk_timer(
                            channel_id, game.current_player(), game.state["turn_count"]
                        )
                    )
            except Exception as e:
                print(f"AFK Timer Error: {e}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnoCog(bot))
