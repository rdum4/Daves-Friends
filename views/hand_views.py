import discord

from views.base_views import BaseViews
from models.deck import format_card, Card


class HandViews(BaseViews):
    def hand_embed(self, hand: list[Card]) -> discord.Embed:
        cards_display = []
        for index, card in enumerate(hand):
            cards_display.append(f"**{index}**  →  {format_card(card)}")

        embed = self._build_embed(
            title="Your Hand",
            desc="\n".join(cards_display),
            color=self.get_random_color(),
            gif=False,
            footer=False,
            time_stamp=True,
            random_gif=False,
            author=False
        )

        return embed