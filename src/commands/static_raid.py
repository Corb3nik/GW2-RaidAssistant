from discord.ext import commands
from views.static_run_embed import StaticRunEmbed
from core.constants import *
from models import Raid


@commands.command(name='static')
async def static_raid(ctx, description=None, time=None):
    """
    Create a new raid announcement for the static
    """

    new_raid = Raid(description=description, time=time, composition=None)

    embed = StaticRunEmbed(new_raid)
    message = await ctx.send("", embed=embed)

    new_raid.message_id = message.id
    new_raid.save()

    for emoji in DEFAULT_REACTIONS:
        await message.add_reaction(emoji)
