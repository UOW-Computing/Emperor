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
from typing import Mapping, Optional, List

class MyHelpCommand(commands.HelpCommand):


    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]):
        """
        Sends an embed with all the commands for the server
        
        Args:
            mapping (Mapping[Optional[Cog], List[commands.Command]]): List of all Cogs and commands
        
        Retruns:
            discord.Embed - contains all commands formated correctly
        
        """
        embed = discord.Embed(title="Emperor Help", color=self.context.bot.config.COLOUR)

        description = f"""{self.context.bot.description}
        Using `{self.context.clean_prefix}help` shows this embed again.
        NOTE: Slash Commnads will not work with `{self.context.clean_prefix}help [command]`."""

        for cog, command in mapping.items():
            cog_name = getattr(cog, "qualified_name", "No Category")

            if cog_name in ["Dev", "Event", "Help", "No Category"]:
                continue
            
            # Figure out how many commands are
            # inside the cog
            commands_list = cog.get_commands() if not (cog is None) else command
            
            app_commands_union = cog.get_app_commands() if not (cog is None) else []
            num = 0
            for app_command in app_commands_union:
                if isinstance(app_command, app_commands.Command):
                    num += 1
                if isinstance(app_command, app_commands.Group):
                    num += len(app_command.commands)
            
            embed.add_field(name=f'{cog_name} ({len(commands_list) + num})',
                                value=cog.description if not (cog is None) else "Nothing here",
                                inline=False)
                
        embed.description = description
        embed.set_author(name=self.context.bot.user.display_name, icon_url=self.context.bot.user.display_avatar)
        embed.set_footer(text=f'run by {self.context.author.display_name} | ID: {self.context.author.id}',
                         icon_url=self.context.author.display_avatar)
        
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command),
                              color=self.context.bot.config.COLOUR)
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
        
    async def send_cog_help(self, cog: commands.Cog) -> None:
        """Gathers information about the cog and sends an embed with the information.

        Args:
            cog (Cog): The cog the information is about.
        """
        channel = self.get_destination()
        
        embed = discord.Embed(title=f'{cog.qualified_name}', color=self.context.bot.config.COLOUR)
        
        # embed.add_field(name="Commands", value="Commands that can be run through the prefix", inline=False)
        for command in cog.walk_commands():
            embed.add_field(name=command.name, value=command.description, inline=True)
        
        # embed.add_field(name="Slash Commands", value="Commands that are built into the client by the bot", inline=False)
        for command in cog.walk_app_commands():
            if isinstance(command, app_commands.Group):
                continue
            embed.add_field(name=f'{command.qualified_name}', value=command.description, inline=True)
        
        embed.description = cog.description
        embed.set_author(name=self.context.bot.user.display_name, icon_url=self.context.bot.user.display_avatar)
        embed.set_footer(text=f'run by {self.context.author.display_name} | ID: {self.context.author.id}',
                         icon_url=self.context.author.display_avatar)
        
        await channel.send(embed=embed)

class Help(commands.Cog, description="Shows this message."):
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
