"""
Provides a view into a player's hand.
"""

import discord

from views.base_views import BaseViews
from models.deck import format_card, Card


class HandViews(BaseViews):
    """
    The hand view for displaying information about a player's hand.
    """

    def hand_embed(
        self, hand: list[Card], optional_message: str | None = None
    ) -> discord.Embed:
        """
        Creates an embed for a player's hand based on the contents of their hand and an optional
        message.
        """
        cards_display = []
        for index, card in enumerate(hand):
            cards_display.append(f"**{index}**  →  {format_card(card)}")

        msg = "\n".join(cards_display)

        if optional_message:
            msg += "\n" + optional_message

        embed = self._build_embed(
            title="Your Hand",
            desc=msg,
            color=self.get_random_color(),
            gif=False,
            footer=False,
            time_stamp=True,
            random_gif=False,
            author=False,
        )

        return embed
