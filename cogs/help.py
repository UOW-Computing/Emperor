import os
import json
import discord


from discord.ext import commands
from src.ServerUtils import Utils


class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help", description=f"Use `e!help` for this embed again!"
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
                    cog_commands += f"• `{cmd_usage}`\n{cmd_description}\nCooldown is `{cmd_cooldown}`\n\n"

            embed.add_field(name=cog, value=cog_commands, inline=True)

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
    await bot.add_cog(Help(bot))


async def teardown(bot):
    bot.help_command = bot._default_help_command
