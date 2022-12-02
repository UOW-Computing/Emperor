"""
General Category.

Holds command that do not belong to a specific category.

"""

import discord

from discord.ext import commands
from src.util import GUILD_ID


class General(commands.Bot):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="hello",
                            description="Says Hello back", guild_ids=GUILD_ID)
    async def hello(self, ctx):
        ctx.respond(f'<@{ctx.author.id}>, hello!')



def setup(bot):
    bot.add_cog(General(bot))