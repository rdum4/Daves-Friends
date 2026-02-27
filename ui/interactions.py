"""
Provides an implementation of the Discord UI view for the bot.
"""

import discord.ui


class Interactions(discord.ui.View):
    """
    Configures the Discord UI view for the bot, setting the timeout to None.
    """

    def __init__(self):
        super().__init__(timeout=None)
