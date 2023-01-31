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

from datetime import datetime as dt
from discord.utils import format_dt
from discord.ext import commands
from discord import app_commands


class Main(commands.Cog):
    """
    Main Cog

    Holds all the commands that do not fit a specific catagory
    """

    def __init__(self, bot):
        self.bot = bot

    info_group = app_commands.Group(
        name="info", description="Gives information about server and member."
    )

    tutorials_group = app_commands.Group(
        name="tutorials", description="Holds all the tutorials comand"
    )

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.maincog", "MainCog cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.maincog", "MainCog cog was unloaded")

    async def cog_command_error(self, ctx, error):
        print(error)

    async def cog_app_command_error(self, interaction, error):
        self.bot.lj.warn(
            f"emperor.cogs.maincog.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )
        await interaction.response.send_message(f"<@{interaction.user.id}>, {error}")

    async def __count_online_members(self, guild: discord.Guild) -> int:
        """Counts the number of online members in the guild

        Args:
            guild (discord.Guild): The guild to get the members from

        Returns:
            int: The number of online (online & dnd) members
        """

        # Go through the guild members
        # Check if their status is dnd/online
        # increment if so
        num = 0

        possibleStatus = [
            discord.Status.dnd,
            discord.Status.do_not_disturb,
            discord.Status.online,
        ]

        for member in guild.members:
            if member.status in possibleStatus:
                num += 1

        # Return the number of online/dnd members
        return num

    def __count_bot(self, guild: discord.Guild) -> int:
        """Counts the number of bots in the guild

        Args:
            guild (discord.Guild): The guild to count the bots from

        Returns:
            int: The number of bots in the guild
        """
        num = 0
        for member in guild.members:
            if member.bot:
                num += 1

        return num

    def __count_top_three_roles(self, member: discord.Member) -> str:
        roles = ""
        rolelen = len(member.roles)

        for i in range(1, rolelen, 1):
            roles += f"<@&{member.roles[-i].id}>"

        return roles

    def __count_emojis(self, guild: discord.Guild) -> str:
        """
        Counts the number of emojis in the server

        Args:
            guild (discord.Guild): The guild to count the emojis from

        Returns:
            str: The emojis as <:emoji_name:emoji_id> or the string number of emojis
        """

        # Checking to see if the guild has 0 emojis
        if len(guild.emojis) == 0:
            return "0"

        # Go through the guild emojis
        # Add them into a string for later use
        emojilist = " ".join([f"<:{emoji.name}:{emoji.id}>" for emoji in guild.emojis])

        # Making sure that the limit in embeds is not
        # broken
        if len(emojilist) >= 1024:
            return str(len(guild.emojis))

        # If limit is isn't broken
        # send the emojis
        return emojilist

    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction) -> None:
        """
        A simple hello command.
        Used to test out if Application commands (Slash Commands) are working

        Params:
            interaction: the event that causes this command to execute

        """
        await interaction.response.send_message(f"<@{interaction.user.id}>, hello!")

    @info_group.command(
        name="server",
        description="Collects and sends an embed with information about the server",
    )
    async def info_server(self, interaction: discord.Interaction) -> None:
        """Collects and sends an embed with information about the server

        Args:
            interaction (discord.Interaction): The trigger for this command

        Returns:
            Embed (discord.Embed): Contains the information gathered on
                the guild
        """

        # Uses the default logo
        # If the guild doesn't have one
        icon_file = None
        guild = interaction.guild
        if guild.icon is None:
            icon_file = discord.File("res/discordLogo.png", filename="logo.png")

        # Making the embed with the pre-defined colour
        # and setting the title & description
        # with guild name and description
        server_embed = discord.Embed(
            color=self.bot.config.COLOUR,
            title=guild.name,
            description=guild.description,
        )
        img_url = guild.icon if guild.icon is not None else "attachment://logo.png"
        server_embed.set_thumbnail(url=img_url)
        server_embed.add_field(name="Owner", value=f"<@{guild.owner_id}>", inline=True)

        # If the guild has a banner
        # set the image to it
        if guild.banner:
            server_embed.set_image(url=guild.banner.url)

        # Display the total member count with online and offline
        server_embed.add_field(
            name="Members",
            value=f"{guild.member_count} ({await self.__count_online_members(guild)} online)",
            inline=True,
        )

        # Get the number of bots in the server
        server_embed.add_field(name="Bots", value=self.__count_bot(guild), inline=True)

        # Get the roles and make them mentionable
        server_embed.add_field(name="Roles", value=len(guild.roles), inline=True)

        # Get the number of channels in the server
        server_embed.add_field(name="Channels", value=len(guild.channels), inline=True)

        # Use the string value from __count_emojis
        # to fill in the Emojis field
        server_embed.add_field(
            name="Emojis", value=self.__count_emojis(guild), inline=True
        )

        # Guild id and when created as footer
        server_embed.set_footer(
            text=f'ID: {guild.id} | Server Created • {(guild.created_at.strftime("%Y/%m/%d %H:%M %p"))}'
        )

        # Attach the file, only if the guild
        # does not have an icon
        if guild.icon is not None:
            await interaction.response.send_message(embed=server_embed)
        else:
            await interaction.response.send_message(file=icon_file, embed=server_embed)
        # await interaction.response.send_message('This is a `/log server`')

    @info_group.command(name="member", description="Gets information about the user")
    async def info_member(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        """
        Gets the information about the user and sends it as an embed

        Args:
            member (discord.Member): The user to collect information about

        Returns:
            Embed (discord.Embed): Information collected on the user
        """

        # Create the embed
        # Information is gathered from discord.Member
        # properties
        member_embed = discord.Embed(
            color=self.bot.config.COLOUR,
            title="Member Information",
            description=f"""Name: `{member.name}{f" ({member.display_name})" if member.display_name != member.name else ""}`
            Joined Discord on: {format_dt(member.created_at)}
            Joined Server on: {format_dt(member.joined_at)}
            Roles: {self.__count_top_three_roles(member)}""",
        )

        # Set the image to their avatar
        member_embed.set_image(url=member.display_avatar.url)

        # Simple footer filler
        member_embed.set_footer(
            text=f'{self.bot.user.name} | {dt.now().strftime("%d %B %Y %H:%M %p")}',
            icon_url=self.bot.user.display_avatar,
        )

        await interaction.response.send_message(embed=member_embed)

    # All Tutorials commands #
    @tutorials_group.command(name="git", description="Tutorials for Git")
    async def git(self, interaction: discord.Interaction) -> None:
        """Sends an embed containg tutorials for Git

        Args:
            interaction (discord.Interaction): The interacion which caused this to happen
        """
        icon_file: discord.File = discord.File("res/gitLogo.png", "gitLogo.png")

        git_embed = {
            "description": """
Looking to learn Git?

Install Git from [here](https://git-scm.com/downloads).

*Some of the tutorials contain GitHub as well.*

List of text based tutorials:
- [Git Documentation](https://git-scm.com/docs/gittutorial) (*Best*)
- [W3School](https://www.w3schools.com/git/default.asp)
- [FreeCodeCamp](https://www.freecodecamp.org/news/best-git-tutorial/)
- [Git Book](https://git-scm.com/book) (*Best*)

List of Youtube tutorials:
- [FreeCodeCamp](https://www.youtube.com/watch?v=RGOj5yH7evk)
- [The Net Ninja, Git Playlist](https://www.youtube.com/playlist?list=PL4cUxeGkcC9goXbgTDQ0n_4TBzOO0ocPR)


""",
            "thumbnail": {"url": "attachment://gitLogo.png"},
            "footer": {"text": "Emperor"},
            "title": "Git",
        }

        await interaction.response.send_message(
            embed=discord.Embed.from_dict(git_embed), file=icon_file
        )

    @commands.command(
        name="uptime",
        description="Shows long the bot has been online for"
    )
    async def uptime(self, ctx):
        """
        Shows how long the bot has been online for
        """

        await ctx.send(
            f"The bot has been online for: <t:{int(dt.timestamp(self.bot.uptime))}:R>"
        )


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

    await bot.add_cog(Main(bot), guilds=guild_objects)
