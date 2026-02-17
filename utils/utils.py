import discord


def require_channel_id(interaction: discord.Interaction) -> int:
    cid = interaction.channel_id
    if cid is None:
        raise RuntimeError("This command must be used in a server channel (not DMs).")
    return cid


def mention(user_id: int) -> str:
    return f"<@{user_id}>"
