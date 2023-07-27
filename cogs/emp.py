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

from datetime import datetime
from discord.ext import commands
from discord import app_commands
from github import Github


class Emp(
    commands.Cog,
    name="Emperor",
    description="All commands relate to emperor, and developers working on emperor",
):
    """
    Holds all the /emperor commands
    All commands relate to the emperor, and developers working
    on the emperor.
    """
    
    emperor_group = app_commands.Group(name="emperor",
                                   description="All commands relate to emperor, and developers working on emperor")

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.botcog", "BotCog cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.botcog", "BotCog cog was unloaded")

    async def cog_app_command_error(self, interaction, error):
        self.bot.lj.warn(
            f"emperor.cogs.bot.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )
        await interaction.response.send_message(f"<@{interaction.user.id}>, {error}")

    @emperor_group.command(name="contribute", description="Contribute to Emperor")
    async def contribute(self, interaction: discord.Interaction) -> None:
        """
        Instructions on how to contribute to Emperor

        Params:
                interaction: the event that causes this command to execute

        Returns
                Nothing
        """
        embed_json = {
            "title": "Contribute to Emperor",
            "description": """**Before you can start contributing, you must have some knowledge of python.**
You can look [here](https://github.com/UOW-Computing/Emperor/discussions/27) for a guide.
To learn Python or Git, you can do `/tutorials python` or `/tutorials git`.
Read [Getting Started](https://github.com/UOW-Computing/Emperor/discussions/46) before contributing. 

Once you have Emperor locally, you must have some kind of idea that you wish to add into the bot. 
Develop that idea and do a PR (Pull request) so the current contributors can have a look at it.

If you do not have an idea, you can look at [issues](https://github.com/UOW-Computing/Emperor/issues) and fix/add them!

Remember: **Do not be scared to contribute, no one will make a fool of you, we will help make it a reality**""",
            "color": 10509236,
            "timestamp": str(datetime.now()),
            "author": {
                "name": "nukestye",
                "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png",
            },
            "footer": {
                "text": "Emperor",
                "icon_url": "https://cdn.discordapp.com/embed/avatars/3.png",
            },
            "fields": [
                {
                    "name": "Repo",
                    "value": "[GitHub Link](https://github.com/UOW-Computing/Emperor/)",
                    "inline": False,
                }
            ],
        }

        embed = discord.Embed.from_dict(embed_json)

        await interaction.response.send_message(embed=embed)

    # pylint: disable=too-many-arguments
    # Anything related to Github goes here!
    # PyGithub Wrapper -> Github REST API
    @emperor_group.command(
        name="issue", description="Creates an Issue on Emperor's Repo."
    )
    async def create_issue(
        self,
        interaction: discord.Interaction,
        title: str,
        body: str,
        assignee: str,
        label: str,
    ) -> None:
        """
        Creates an issue, requires title, topic, assignee and label.


        Args:
                title (str): title of the Issue, use Emperor's Guidelines
                body (str): Issue at question, Emperor's Guidelines
                assignee (str): Author
                label (str): Use labels accordingly, check Emperor's Issue/PR templates

        Returns:
                Nothing
        """
        # pylint: enable: too-many-arguments

        # github_connection = Github("your token") - > example of how to establish a connection

        # Creates a session with Github using you token
        github_connection = Github(f"{self.bot.config.GITHUB_KEY}")

        # Fetches Emperor's repo from the connection above
        emperor_repo = github_connection.get_repo("UoW-Computing/Emperor")

        # Creates the issue with the parameters parsed from the slash command /create_issue
        emperor_repo.create_issue(
            title=title, body=body, assignee=assignee, labels=[label]
        )

        # Creates the Embed, this is will need to be refactored into a function.
        # Hardcoding the Embed it's not a good practice.
        github_embed = {
            "description": f"""

Your issue can be found [here](https://github.com/UOW-Computing/Emperor/issues).

*Please, make sure you follow the [Bug Report Guidelines](https://github.com/UOW-Computing/Emperor/blob/master/.github/ISSUE_TEMPLATE/bug_report.md)*

**Title**:\n {title}

**Description**:\n {body}

**Assignee**:\n {assignee}

""",
            "thumbnail": {"url": "attachment://discordLogo.png"},
            "footer": {"text": "Emperor"},
            "title": "Issue Created",
        }
        # sends the Json above into a Embed
        await interaction.response.send_message(
            embed=discord.Embed.from_dict(github_embed)
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

    await bot.add_cog(Emp(bot), guilds=guild_objects)
