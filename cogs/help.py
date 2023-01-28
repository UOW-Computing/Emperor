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
from src.ServerUtils import Utils


class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help", description=f"Use `e!help` for this embed again!\n"
        )
        # Get help.json
        data = Utils.read_from_json("res/json/help.json")

        for cog in data:
            cog_commands = ""
            for command in data[cog]:
                for i in range(len(data[cog][command])):

                    # Get all the information
                    cmd_usage = data[cog][command][i]["usage"]
                    cmd_description = data[cog][command][i]["description"]
                    cmd_cooldown = data[cog][command][i]["cooldown"]

                    # Format the information and add it to help
                    cog_commands += f"• `{cmd_usage}`\n	{cmd_description}.\n	Cooldown is `{cmd_cooldown}`\n"

            embed.description += f"**{cog}**\n {cog_commands}\n"

        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        # Focus here
        # Setting the cog for the help
        help_command = MyHelpCommand()
        help_command.cog = self  # Instance of YourCog class
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
