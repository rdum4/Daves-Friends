"""
Simple functions for other functions to use.
"""

import discord


def require_channel_id(interaction: discord.Interaction) -> int:
    """
    Checks if an interaction is in a server channel. If not, throw an error.
    """

    cid = interaction.channel_id
    if cid is None:
        raise RuntimeError("This command must be used in a server channel (not DMs).")
    return cid


def mention(user_id: int) -> str:
    """
    Creates a mention for a user by ID using the Discord mention format.
    """
    return f"<@{user_id}>"
