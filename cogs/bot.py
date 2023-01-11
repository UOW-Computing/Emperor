import discord

from discord.ext import commands
from discord import app_commands
from datetime import datetime


class BotCog(
    commands.GroupCog,
    group_name="emperor",
    description="All commands relate to emperor, and developers working on emperor",
):
    """
    Holds all the /emperor commands
    All commands relate to the emperor, and developers working
    on the emperor.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.botcog", "BotCog cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.botcog", "BotCog cog was unloaded")

    async def cog_check(self, ctx):
        # checks that apply to every command in here
        return True

    async def bot_check_once(self, ctx):
        # check that apply to every command but is guaranteed to be called only once
        return True

    async def cog_command_error(self, ctx, error):
        # error handling to every command in here
        pass

    async def cog_app_command_error(self, interaction, error):
        self.bot.lj.warn(
            f"emperor.cogs.bot.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )
        await interaction.response.send_message(f"<@{interaction.user.id}>, {error}")

    async def cog_before_invoke(self, ctx):
        # called before a command is called here
        pass

    async def cog_after_invoke(self, ctx):
        # called after a command is called here
        pass

    @app_commands.command(name="contribute", description="Contribute to Emperor")
    async def hello(self, interaction: discord.Interaction) -> None:
        """
        Instructions on how to contribute to Emperor

        Params:
                interaction: the event that causes this command to execute

        Returns
                Nothing
        """
        embedJSON = {
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

        embed = discord.Embed.from_dict(embedJSON)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    # Make an discord.Object for each
    # guild in the list
    guild_objects: list[discord.Object] = []
    for guild in bot.config.GUILD_ID:
        guild_objects.append(discord.Object(id=guild))

    await bot.add_cog(BotCog(bot), guilds=guild_objects)
