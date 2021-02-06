from views.raid_embed import RaidEmbed
from discord.ext import commands
from core.constants import *
from core.utils import get_custom_emoji
from models.raid import Raid


@commands.command(name='create')
async def create_raid(ctx, title=None, description=None, time=None):
    """
    Create a new raid announcement
    """

    embed = RaidEmbed(title, description, time)
    message = await ctx.send("", embed=embed)

    headcount = get_custom_emoji(ctx, "headcount") or RAISED_HANDS
    await message.add_reaction(headcount)
    await message.add_reaction(ALARM_CLOCK)
