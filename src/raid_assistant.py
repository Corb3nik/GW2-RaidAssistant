import discord
from discord import Emoji
import os
from collections import defaultdict
from views.raid_embed import RaidEmbed
from core.constraint_solver import ConstraintSolver
from core.constants import *
from commands import create_raid, static_raid
from models import *


class RaidAssistant(discord.ext.commands.Bot):

    raid_messages = {}

    async def on_ready(self):
        print("Logged in as {}!".format(self.user))

    async def get_user_raid_roles(self, message):
        raid_roles_per_user = defaultdict(list)
        for reaction in message.reactions:

            if reaction.emoji not in ROLE_REACTIONS:
                continue

            users = await reaction.users().flatten()
            for user in users:

                if user.id == self.user.id:
                    continue

                raid_roles_per_user[user.name] = raid_roles_per_user[user.name] + \
                    [reaction.emoji]

        missing_player_id = 1
        while len(raid_roles_per_user) < SQUAD_LIMIT:
            raid_roles_per_user["Missing player #{}".format(
                missing_player_id)] = ROLE_REACTIONS
            missing_player_id += 1

        return raid_roles_per_user

    async def on_raw_reaction_add(self, payload):

        if payload.user_id == self.user.id:
            return

        raid: Raid = Raid.get_or_none(Raid.message_id == payload.message_id)
        if not raid:
            return

        if payload.emoji.name == SUBMIT_REACTION:
            await self.find_composition(payload)

        if payload.emoji.name == ALARM_CLOCK and raid.organiser_id == str(payload.user_id):
            await self.wakeup(payload)

    async def find_composition(self, payload):
        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        curr_raid_info = Raid.get_or_none(Raid.message_id == message.id)

        # Intermediate loading message
        curr_raid_info.composition = "Calculating..."
        new_embed = RaidEmbed(curr_raid_info)
        await message.edit(embed=new_embed)

        raid_roles_per_user = await self.get_user_raid_roles(message)

        solver = ConstraintSolver(ROLE_REACTIONS, raid_roles_per_user)
        solutions = solver.get_solutions()
        solution = next(solutions, None)

        if not solution:
            curr_raid_info.composition = "Failed. Could not generate a team composition."
        else:
            entries = []
            for key, user_id in solution.items():
                if "Missing player" in user_id:
                    user_id = ""

                entries += ["{} {}".format(key, user_id)]
            curr_raid_info.composition = '\n'.join(sorted(entries))

        new_embed = RaidEmbed(curr_raid_info)
        await message.edit(embed=new_embed)

        curr_raid_info.save()

    async def wakeup(self, payload):
        channel = await self.fetch_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        users = set()
        for reaction in message.reactions:
            emoji = reaction.emoji
            custom = isinstance(emoji, Emoji) and emoji.name == "headcount"
            is_raised_hands = emoji == RAISED_HANDS
            if custom or is_raised_hands:
                async for user in reaction.users():
                    if user.id != self.user.id:
                        users.add(user.mention)

        await channel.send("{} wake up buttercup(s) we're raiding".format(", ".join(users)))


if __name__ == '__main__':

    # Initialize database
    BaseModel._meta.database.create_tables([Raid])

    bot = RaidAssistant(command_prefix='!raid ')
    bot.add_command(static_raid)
    bot.add_command(create_raid)
    bot.run(os.environ['DISCORD_BOT_TOKEN'])
