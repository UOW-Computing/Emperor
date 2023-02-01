"""
Emperor, discord bot for school of computing
Copyright (C) 2022-2023  School of Computing Dev Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord

from discord.ext import commands
from discord import RawReactionActionEvent
from src.ServerUtils import Utils


class Event(commands.Cog):
    """
    Event class

    All discord events exculding on_ready and on_message are handled here
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.event", "Event cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.event", "Event cog was unloaded")

    async def on_error(self, event):
        """
        Whenever a problem occurs with any event commands,
        this function gets executed

        Args:
            event: The error caused
        """
        self.bot.lj.error("emperor.cogs.event", f"{event}")

    async def process_reaction(
        self, payload: RawReactionActionEvent, return_type=None
    ) -> None:
        """
        Process the reaction, decides to add or remove a role if it is a reaction message

        Args:
            payload (RawReactionActionEvent): The event that called the function
            return_type (str, optional): What to do with the role (add or remove). Defaults to None.
        """

        reaction_roles = Utils.read_from_json("res/json/reaction_roles.json")

        guild = self.bot.get_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)

        # If the bot was the one to
        # react then do nothing
        if user.bot:
            return

        if str(payload.guild_id) in reaction_roles.keys():
            if str(payload.message_id) in reaction_roles[str(payload.guild_id)]:
                if user is None:
                    self.bot.lj.warn(
                        "emperor.cogs.event.process_reaction", "User is None"
                    )
                    return

                # Check if the emoji that was reacted
                # is unicode
                if payload.emoji.is_unicode_emoji():
                    role = guild.get_role(
                        reaction_roles[str(payload.guild_id)][str(payload.message_id)][
                            str(payload.emoji.name)
                        ]
                    )
                else:
                    role = guild.get_role(
                        reaction_roles[str(payload.guild_id)][str(payload.message_id)][
                            str(payload.emoji.id)
                        ]
                    )

                # What happens if the role could not be found
                if role is None:
                    self.bot.lj.warn(
                        "emperor.cogs.event.process_reaction",
                        f"An invalid role ID was provided in `reaction_roles` for message with ID: {payload.message_id}",
                    )

                # Add the role
                elif return_type == "add":

                    self.bot.lj.log(
                        "emperor.cogs.event.process_reaction",
                        f"Role: {role.name} has been given to {user.name}",
                    )

                    await user.add_roles(role)

                # Remove the role
                elif return_type == "remove":

                    self.bot.lj.log(
                        "emperor.cogs.event.process_reaction",
                        f"Role: {role.name} has been removed from {user.name}",
                    )

                    await user.remove_roles(role)
                else:
                    self.bot.lj.warn(
                        "emperor.cogs.event",
                        "Invalid reaction type was provided in `process_reaction`.",
                    )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """
        Whenever a reaction was added into a message, its called
        """

        await self.process_reaction(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """
        Whenever a reaction was removed into a message, its called
        """
        await self.process_reaction(payload, "remove")


async def setup(bot):
    """
    Setup function for the cog

    Args:
        bot (discord.ext.commands.Bot): Instance of the bot class
    """

    # Make an discord.Object for each
    # guild in the list
    guild_objects: list[discord.Object] = []
    for guild in bot.config.GUILD_ID:
        guild_objects.append(discord.Object(id=guild))

    await bot.add_cog(Event(bot), guilds=guild_objects)
