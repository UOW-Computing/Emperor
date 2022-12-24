"""
General Category.

Holds command that do not belong to a specific category.

"""
# pylint: disable=eval-used

import os
import json
import random
import discord
import requests


from discord.ext import commands
from discord.commands import Option


class General(commands.Cog):
    """
    General Category for all commands that anyone can use.

    Contains the following commands:
     - hello
     - server TODO: Change command into info and have sub commands server, channel, user and message
     - reddit search

    """
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

        server_embed = discord.Embed(title=guild.name,
                                     description=guild.description)
        img_url = guild.icon if guild.icon is not None else 'attachment://logo.png'
        server_embed.set_thumbnail(url=img_url)
        server_embed.add_field(name='Owner',
                               value=f'<@{guild.owner.id}>', inline=True)

        server_embed.add_field(name='Members',
                               value=guild.member_count, inline=True)
        if guild.icon is not None:
            await ctx.response.send_message(embed=server_embed)
        else:
            await ctx.response.send_message(file=discordfile, embed=server_embed)

    @commands.slash_command(name="reddit",
                            description="Search subreddits on reddit",
                            guild_ids=eval(os.getenv('GUILD_ID')))
    async def reddit_search(self, ctx, subreddit: Option(str, "Subreddit to look through",
                                                         required=False)):
        """
        Gets a random post from user inputted subreddit

        Params:
            subreddit: Subreddit to get the post from
        """

        def check(msg):
            if msg.author == ctx.author and msg.channel == ctx.channel:
                if msg.content != "":
                    return True
                else:
                    return False

        if subreddit is None:
            subreddit_ask = await ctx.channel.send("Please enter the subreddit to look through")

            message = await ctx.bot.wait_for('message', check=check)

            subreddit = message.content

            await subreddit_ask.delete()
            await message.delete()

        subreddit_link = f'https://www.reddit.com/r/{subreddit}/hot/.json?sort=top&t=week&limit=10'

        # Asking for a random post
        r = requests.get(subreddit_link, headers={'User-agent': 'Emperor'})

        # Checking if the subreddit does exist
        json_data = json.JSONDecoder().decode(r.text)

        if 'error' in json_data:
            await ctx.channel.send("The subreddit does not exist, or has no content.")
            return

        post_data = json_data['data']['children'][random.randint(0, 10)]

        # Check if the post is sfw
        if post_data['data']['over_18']:
            await ctx.followup.send("Bot cannot post 18+ content.", ephemeral=True)
            return

        post_data['data']['title'] = post_data['data']['title'].replace(u"\u2018", "'").replace(u"\u2019", "'")

        post_title = f"[{post_data['data']['title']}](https://www.reddit.com{post_data['data']['permalink']})"

        post_embed = discord.Embed(description=f"{post_title}\nBy *{post_data['data']['author']}*",
                                   color=9240816)
        post_embed.set_footer(text=f"👍 {post_data['data']['ups']} | 💬 {post_data['data']['num_comments']}")
        post_embed.set_image(url=post_data['data']['url'])
        # postEmbed.set_author(name=data['data']['author'])

        await ctx.respond(embed=post_embed)


def setup(bot):
    bot.add_cog(General(bot))
