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
import random
import discord
import aiohttp
import openai
from src.ServerUtils import Utils

from bs4 import BeautifulSoup
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from typing import List, Tuple
from src.errors.checks import DisabledCommand


class API(commands.Cog):
    """
     API Cog

    Holds all the commands that connect to APIs for stuff
    """

    def __init__(self, bot):
        self.bot = bot
        openai.api_key = bot.config.OPENAI_KEY
        
    duckduckgo = app_commands.Group(
        name="duckduckgo",
        description="Holds all duckduckgo commmands"
    )

    # API Related #
    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.api", "API cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.api", "API cog was unloaded")

    async def cog_app_command_error(self, interaction, error):

        self.bot.lj.warn(
            f"emperor.cogs.api.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )

        # Checks if the command is on cooldown,
        # if so tell the user
        if isinstance(error, app_commands.CommandOnCooldown):
            on_cooldown: str = \
                f"Currently on cooldown, try again in <t:{int(datetime.now().timestamp()+error.retry_after)}:R>."
            await interaction.response.send_message(
                on_cooldown, delete_after=error.retry_after
            )
            return

        if isinstance(error, DisabledCommand):
            await interaction.response.send_message(
                f"{error.args}\nPlease ask staff to enable, if need be.",
                ephemeral=True
            )
            return

        # Handles the InteractionAlreadyBeenResponsed to Exception
        try:
            await interaction.response.send_message(
                f"<@{interaction.user.id}>, {error}"
            )
        except Exception as exc:
            await interaction.followup.send(f"<@{interaction.user.id}>, {error}\n{exc}")


    # Implementing on and off for commands
    def is_on():
        def _extras_json() -> dict:
            return Utils.read_from_json("res/json/extras.json")
        
        def predicate(interaction: discord.Interaction, bot: discord.ext.commands.Bot) -> bool:
            
            if interaction.command.extras['command_signature'] in _extras_json()['disabled_commands']:
                raise DisabledCommand("Command has been disabled, therefore cannot be executed.")
            else:
                return True
        
        async def decorator(interaction: discord.Interaction):
            
            bot = interaction.client
            
            return predicate(interaction, bot)
        
        return app_commands.check(decorator)

    # Reddit Related #
    @app_commands.command(
        name="reddit",
        description="Looks through subreddits given by the user",
        extras=dict({
            'command_signature': 'reddit_search'
        })
    )
    # Checking to see if this command can be run
    @is_on()
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def reddit(self, interaction: discord.Interaction, subreddit: str):
        """
        Gets a random post from user inputted subreddit

        Params:
            subreddit: Subreddit to get the post from
        """

        subreddit_link = (
            f"https://www.reddit.com/r/{subreddit}/hot/.json?sort=top&t=week&limit=10"
        )

        # Get the post
        # Choose a random post
        # Send it in as an embed
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(subreddit_link) as response:

                # Convert to json
                json_data = await response.json()

                # Checking if the subreddit does exist
                if "error" in json_data:
                    await interaction.response.send_message(
                        "The subreddit does not exist, or has no content."
                    )
                    return

                post_data = json_data["data"]["children"][
                    random.randint(0, len(json_data["data"]["children"]))
                ]

                # Check if the post is sfw
                if post_data["data"]["over_18"]:
                    await interaction.response.send_message(
                        "Emperor cannot post 18+ content at all.", ephemeral=True
                    )
                    return

                post_data["data"]["title"] = (
                    post_data["data"]["title"]
                    .replace("\u2018", "'")
                    .replace("\u2019", "'")
                )

                post_title = f"[{post_data['data']['title']}](https://www.reddit.com{post_data['data']['permalink']})"

                post_embed = discord.Embed(
                    description=f"{post_title}\nBy *{post_data['data']['author']}*",
                    color=self.bot.config.COLOUR,
                )
                post_embed.set_footer(
                    text=f"👍 {post_data['data']['ups']} | 💬 {post_data['data']['num_comments']}"
                )
                post_embed.set_image(url=post_data["data"]["url"])
                # postEmbed.set_author(name=data['data']['author'])

                await interaction.response.send_message(embed=post_embed)

    # DuckDuckGo Related #
    async def __get_search_results(self, query: str) -> List[Tuple[str, str]]:
        """
        Send a search query to the DuckDuckGo search engine and return the links and titles
        of the search results.

        Parameters:
        - query: the search query to send to the search engine.

        Returns:
        - A list of tuples, where each tuple contains the link and title for a single search result.
        """
        # Clean up the query string
        query = "+".join(query.strip().split())

        # Send an HTTP GET request to the DuckDuckGo search engine
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(
                f"https://duckduckgo.com/html/?q={query}"
            ) as response:
                data = await response.text()

        # Parse the response data using BeautifulSoup
        soup = BeautifulSoup(data, "html.parser")

        # Find all the search result links
        result_links = soup.select("a.result__a")

        # Extract the link and title for each result
        results = [(link["href"], link.text) for link in result_links]

        return results
    
    
    @duckduckgo.command(
        name="search",
        description="Get search results from DuckDuckGo search",
        extras=dict({
            'command_signature': 'ddg_search'
        })
    )
    @is_on()
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def ddg_search(self, interaction: discord.Interaction, query: str):
        """
        Get search from DuckDuckGo.

        Params:
            query: The parameter for DuckDuckGo search.
        """

        await interaction.response.defer()

        discordfile = None
        guild = interaction.guild
        if guild.icon is None:
            discordfile = discord.File(
                "res/DuckDuckGo Logo- Dax Solo.png", filename="ddg_logo.png"
            )

        results = await self.__get_search_results(query)

        result_embed = discord.Embed(color=self.bot.config.COLOUR)

        desc: str = ""

        result_limit = 0

        for result in results:
            if result_limit < 10:
                desc += f"`{result_limit}` • [{result[1]}](https:{result[0]})\n\n"
                result_limit += 1

        result_embed.description = f' **"{query}"** search results:\n{desc}'

        result_embed.set_footer(text=f"Searched by {interaction.user} | Emperor")
        result_embed.set_author(name="DuckDuckGo")
        result_embed.set_thumbnail(url="attachment://ddg_logo.png")

        await interaction.followup.send(embed=result_embed, file=discordfile)

    @duckduckgo.command(
        name="im_feeling_lucky",
        description="Duckduckgo implementation of Im Feeling Lucky!",
        extras=dict({
            'command_signature': 'ddg_lucky'
        })
    )
    async def im_feeling_lucky(self, interaction, query: str) -> None:
        """
        Send a search query to the DuckDuckGo search engine and return the link and title
        of the first search result.

        Args:
            query: the search query to send to the search engine.

        """
        # Clean up the query string
        query = "+".join(query.strip().split())

        # Send an HTTP GET request to the DuckDuckGo search engine
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(f'https://duckduckgo.com/html/?q={query}') as response:
                data = await response.text()

        # Parse the response data using BeautifulSoup
        soup = BeautifulSoup(data, 'html.parser')

        # Find all the search result links
        result_links = soup.select("a.result__a")

        # Extract the link and title for the first result
        result = result_links[0]
        link = result['href']
        title = result.text

        result_embed = discord.Embed(
            color=self.bot.config.COLOUR,
            title="I'm feeling lucky search!",
            description=f"\n[Click here](https:{link})"
        )

        await interaction.response.send_message(embed=result_embed)

    # chatGPT Related #
    async def __generate_text(self, prompt: str) -> str:
        """Uses the prompt to get the result from ChatGPT 3.0

        Args:
            prompt (str): User input, which is given to ChatGPT 3.0

        Returns:
            str: The response to the prompt given
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        text = response["choices"][0]["text"]
        if text:
            # Send the response to the user in the Discord channel
            return text

        # Send a default message if the response is empty
        return "I'm sorry, I cannot generate a response for this prompt."

    @app_commands.command(
        name="chatgpt",
        description="Generates text using a GPT model",
        extras=dict({
            'command_signature': "gpt_prompt"
        })
    )
    @is_on()
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def gpt(self, interactions: discord.Interaction, prompt: str):
        """Uses ChatGPT to generate a response to a user given prompt

        Args:
            prompt (str): The user given input, to which the response is tailored towards
        """
        
        await interactions.response.send_message("Sorry, currently ChatGPT is disabled.")
        
        return None

        await interactions.response.defer()

        # Generate text using the GPT model
        response = await self.__generate_text(prompt)

        formated_response = f"**Question**: {prompt}\n\n**ChatGPT**: {response}"

        # Send the generated text as a message in the Discord channel
        await interactions.followup.send(content=formated_response)

    # For new Newer features please keep functionallity together#


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

    await bot.add_cog(API(bot), guilds=guild_objects)
