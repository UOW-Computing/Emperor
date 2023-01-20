import discord
import asyncio

from discord import app_commands
from discord.ext import commands


class Admin(commands.Cog):
    """
    Admin cog

    Holds developer commands that should not be run by anyone but the bot owner
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.admin", "Admin cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.admin", "Admin cog was unloaded")

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def bot_check(self, ctx):
        # checks that apply to every command to the bot
        return True

    async def bot_check_once(self, ctx):
        # check that apply to every command but is guaranteed to be called only once
        return True

    async def cog_command_error(self, ctx, error):
        print(error)

    async def cog_app_command_error(self, interaction, error):
        self.bot.lj.warn(
            f"emperor.cogs.admin.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )
        await interaction.response.send_message(f"<@{interaction.user.id}>, {error}")

    async def cog_before_invoke(self, ctx):
        self.bot.lj.log(
            f"emperor.cogs.admin.{ctx.invoked_with}",
            f"{ctx.author.name} has attempted to executed {ctx.invoked_with}",
        )

    async def cog_after_invoke(self, ctx):
        self.bot.lj.log(
            f"emperor.cogs.admin.{ctx.invoked_with}",
            f"{ctx.author.name} has executed {ctx.invoked_with} command",
        )

    @commands.command(name="reload")
    async def reload(self, ctx: commands.Context, cog: str) -> None:
        """
        Allows the changes to be run without having the restart the discord bot
        Reloads all the cogs

        Args:
            cog str: The cog to reload
        """

        try:
            await self.bot.unload_extension("cogs." + cog)
            await self.bot.load_extension("cogs." + cog)

            # The cog was reloaded
            message = await ctx.send(f"The `{cog}` was successfully reloaded")

            # wait 5 seconds then delete
            # both messages
            await asyncio.sleep(5)

            await message.delete()
            await ctx.message.delete()

        except Exception as exc:
            await ctx.send(exc)

    @commands.command(name="load")
    async def load(self, ctx: commands.Context, cog: str) -> None:
        """
        Loads a specifc cog

        Args:
            cog (str): The cog to load
        """
        try:
            await self.bot.load_extension("cogs." + cog)

            # The cog was loaded
            message = await ctx.send(f"The `{cog}` was successfully loaded!")

            # wait 5 seconds then delete
            # both messages
            await asyncio.sleep(5)

            await message.delete()
            await ctx.message.delete()

        except Exception as exc:
            await ctx.send(exc)

    @commands.command(name="unload")
    async def unload(self, ctx: commands.Context, cog: str) -> None:
        """
        Unloads a specifc cog

        Args:
            cog (str): The cog to unload
        """
        try:
            await self.bot.unload_extension("cogs." + cog)

            # The cog was reloaded
            message = await ctx.send(f"The `{cog}` was successfully unloaded")

            # wait 5 seconds then delete
            # both messages
            await asyncio.sleep(5)

            await message.delete()
            await ctx.message.delete()

        except Exception as exc:
            await ctx.send(exc)


async def setup(bot):
    # Make an discord.Object for each
    # guild in the list
    guild_objects: list(discord.Object) = []
    for guild in bot.config.GUILD_ID:
        guild_objects.append(discord.Object(id=guild))

    await bot.add_cog(Admin(bot), guilds=guild_objects)
