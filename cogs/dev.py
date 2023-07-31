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

import asyncio
import discord
import typing

from discord.ext import commands


class Dev(commands.Cog, description="Developer commands"):
    """
    Admin cog

    Holds developer commands that should not be run by anyone
    but the bot dev team
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.dev", "Dev cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.dev", "Dev cog was unloaded")

    # pylint: disable=invalid-overridden-method
    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author) or \
            self.bot.config.STAFF_IDS in ctx.author.roles

    # pylint: enable=invalid-overridden-method

    async def cog_command_error(self, ctx, error):
        print(error)

    async def cog_app_command_error(self, interaction, error):
        self.bot.lj.warn(
            f"emperor.cogs.admin.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )
        await interaction.response.send_message(f"<@{interaction.user.id}>, {error}")
        
        
    async def __delete_messages_after(self, message: discord.Message, ctx: commands.Context):
        # wait 2 seconds then delete
        # both messages
        await asyncio.sleep(2)

        await message.delete()
        await ctx.message.delete()

    @commands.command(name="reload", description="unloads and loads the cog")
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

            await self.__delete_messages_after(message, ctx)

        except Exception as exc:
            message = await ctx.send(exc)
            await self.__delete_messages_after(message, ctx)

    @commands.command(name="load", description="Loads the cog, so commands inside can be used")
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
            
            await self.__delete_messages_after(message, ctx)

        except Exception as exc:
            message = await ctx.send(exc)
            await self.__delete_messages_after(message, ctx)

    @commands.command(name="unload", description="Unloads the cog, prevents commands form being executed/known.")
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

            await self.__delete_messages_after(message, ctx)

        except Exception as exc:
            message = await ctx.send(exc)
            await self.__delete_messages_after(message, ctx)
            
            
    
    # Command used to sync command changes
    @commands.command(name="sync")
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: typing.Optional[typing.Literal["~", "*", "^"]] = None,
    ) -> None:
        """
        Syncs all the commands to the guild/globaly

        Args:
            ctx (commands.Context): The context of the command
            guilds (commands.Greedy[discord.Object]): The Guild where to sync
            spec (typing.Optional[typing.Literal[, optional): Where to sync (global/guild). Defaults to None.
        """
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            message = await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            
            await self.__delete_messages_after(message, ctx)

            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        message = await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
        await self.__delete_messages_after(message, ctx)


async def setup(bot):
    """
    Setup function for the cog

    Args:
        bot (discord.ext.commands.Bot): Instance of the bot class
    """
    # Make an discord.Object for each
    # guild in the list
    guild_objects: list(discord.Object) = []
    for guild in bot.config.GUILD_ID:
        guild_objects.append(discord.Object(id=guild))

    await bot.add_cog(Dev(bot), guilds=guild_objects)
