"""
General Category.

Holds command that do not belong to a specific category.

"""
# pylint: disable=eval-used

import os
import discord

from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="hello",
                            description="Says Hello back",
                            guild_ids=eval(os.getenv('GUILD_ID')))
    async def hello(self, ctx):
        """
        A simple hello command.
        """
        await ctx.respond(f'<@{ctx.author.id}>, hello!')

    @commands.slash_command(name="serverinfo",
                            description="Gives information about the server",
                            guild_ids=eval(os.getenv('GUILD_ID')))
    async def server(self, ctx):
        """
        Gives information about the server the
        command was executed in.

        Params:
                Guild: The guild the command was executed in
        """
        discordfile = None
        guild = ctx.guild
        if guild.icon is None:
            discordfile = discord.File(
                'res/discordLogo.png', filename='logo.png')

        serverEmbed = discord.Embed(title=guild.name,
                                    description=guild.description)
        img_url = guild.icon if guild.icon is not None else 'attachment://logo.png'
        serverEmbed.set_thumbnail(url=img_url)
        serverEmbed.add_field(name='Owner',
                              value=f'<@{guild.owner.id}>', inline=True)

        serverEmbed.add_field(name='Members',
                              value=guild.member_count, inline=True)
        if guild.icon is not None:
            await ctx.response.send_message(embed=serverEmbed)
        else:
            await ctx.response.send_message(file=discordfile, embed=serverEmbed)


def setup(bot):
    bot.add_cog(General(bot))
