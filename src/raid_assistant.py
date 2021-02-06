import discord
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

    def should_process_reaction(self, payload):
        return payload.user_id != self.user.id and \
            payload.emoji.name == SUBMIT_REACTION and \
            Raid.get_or_none(Raid.message_id == payload.message_id)

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

        if not self.should_process_reaction(payload):
            return

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


if __name__ == '__main__':

    # Initialize database
    BaseModel._meta.database.create_tables([Raid])

    bot = RaidAssistant(command_prefix='!raid ')
    bot.add_command(static_raid)
    bot.add_command(create_raid)
    bot.run(os.environ['DISCORD_BOT_TOKEN'])
