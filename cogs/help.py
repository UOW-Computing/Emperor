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
from discord import app_commands
from discord.ext.commands import Cog
from typing import Mapping, Optional, List

class MyHelpCommand(commands.HelpCommand):


    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[commands.Command]]):
        """
        Sends an embed with all the commands for the server
        
        Args:
            mapping (Mapping[Optional[Cog], List[commands.Command]]): List of all Cogs and commands
        
        Retruns:
            discord.Embed - contains all commands formated correctly
        
        """
        embed = discord.Embed(title="Bot help")
        # `mapping` is a dict of the bot's cogs, which map to their commands
        # print(mapping)

        # NOTE: app_commands do not have a normal cooldown
        # attribute, converting all the app_commands
        # into hybrid commands would give them cooldown attribute

        description = ""
        for commands in mapping.items():
            for item in commands:
                # list object is normal text commands
                if item.__class__ == list:
                    for i in item:
                        if i.__class__ is discord.app_commands.Group:
                            continue
                        if i.cog_name in [None, "Admin"]:
                            continue

                        description += f"\n• **e!{i.qualified_name}**: {i.description}"

                # Any Cog object contains app_commands which
                # is slash commands
                elif item.__class__.__base__ == Cog:
                    # Removing Admin and Event Cogs
                    # Contain special commands that cannot be
                    # used by normal users
                    if item.__cog_name__ in ["Admin", "Event"]:
                        continue

                    description += f"\n\n**__{item.__cog_name__}__**\n"

                    for command in item.walk_app_commands():
                        if command.__class__ is discord.app_commands.Group:
                            continue

                        description += f"\n• **/{command.qualified_name}**: {command.description}"

        embed.description = description

        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    """
    Help command that showcases all the possible commands for the bot
    """
    def __init__(self, bot) -> None:
        self.bot = bot

        # Focus here
        # Setting the cog for the help
        help_command = MyHelpCommand()
        help_command.cog = self
        bot.help_command = help_command


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

    await bot.add_cog(Help(bot), guilds=guild_objects)


async def teardown(bot):
    bot.help_command = bot._default_help_command
