import os
import json
import discord


from discord.ext import commands
from src.ServerUtils import Utils


class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help", description=f"Use `e!help` for this embed again!\n"
        )
        # Get help.json
        data = Utils.read_from_json("res/help.json")

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
    # Make an discord.Object for each
    # guild in the list
    guild_objects: list[discord.Object] = []
    for guild in bot.config.GUILD_ID:
        guild_objects.append(discord.Object(id=guild))

    await bot.add_cog(Help(bot), guilds=guild_objects)


async def teardown(bot):
    bot.help_command = bot._default_help_command
