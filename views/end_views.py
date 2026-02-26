import discord

from views.base_views import BaseViews
from models.lobby_model import Lobby
from utils.utils import mention


class EndViews(BaseViews):

    def end_embed(self, lobby: Lobby) -> discord.Embed:
        winner_id = lobby.game.state["winner"]
        hands = lobby.game.state["hands"]
        turn_count = lobby.game.turn_count()

        embed = self._build_embed(
            title="🎉 GAME OVER 🎉",
            desc=f"Winner: {mention(winner_id)}",
            color=self.get_random_color(),
        )

        results_text = ""

        for player_id, cards in hands.items():
            results_text += f"{mention(player_id)} — {len(cards)} cards remaining\n"

        embed.add_field(name="Final Results", value=results_text, inline=False)
        embed.add_field(name="Total Turns Played", value=str(turn_count), inline=False)

        return embed
