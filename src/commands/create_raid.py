from discord.ext import commands
from views.raid_embed import RaidEmbed
from core.constants import *
from models import Raid

@commands.command(name = 'create')
async def create_raid(ctx, description = None, time = None):
    """
    Create a new raid announcement
    """

    new_raid = Raid(description = description, time = time, composition = None)

    embed = RaidEmbed(new_raid)
    message = await ctx.send("", embed=embed)

    new_raid.message_id = message.id
    new_raid.save()

    for emoji in DEFAULT_REACTIONS:
        await message.add_reaction(emoji)
