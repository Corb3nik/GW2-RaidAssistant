from discord.ext.commands import Context
from discord import Emoji
from typing import Optional


def get_custom_emoji(context: Context, name: str) -> Optional[Emoji]:
    for emoji in context.guild.emojis:
        if emoji.name == name:
            return emoji
    return None
