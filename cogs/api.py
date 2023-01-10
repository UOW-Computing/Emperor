import discord
import aiohttp
import random
import openai
from discord.ext import commands
from discord import app_commands
from typing import List, Tuple
from bs4 import BeautifulSoup

class API(commands.Cog):
	"""
	 API Cog

	Holds all the commands that connect to APIs for stuff
	"""

	def __init__(self, bot):
		self.bot = bot
		openai.api_key = bot.config.OPENAI_KEY

	async def cog_load(self):
		self.bot.lj.log('emperor.cogs.api', 'API cog was loaded')

	async def cog_unload(self):
		self.bot.lj.warn('emperor.cogs.api', 'API cog was unloaded')

	async def cog_check(self, ctx):
		# checks that apply to every command in here
		return True

	async def bot_check(self, ctx):
		# checks that apply to every command to the bot
		return True

	async def bot_check_once(self, ctx):
		# check that apply to every command but is guaranteed to be called only once
		return True

	async def cog_command_error(self, ctx, error):
		print(error)


	async def cog_app_command_error(self, interaction, error):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)
		self.bot.lj.warn(f'emperor.cogs.api.{interaction.command.name}',
						 f'<@{interaction.user.id}>, {error}')
		await interaction.response.send_message(f'<@{interaction.user.id}>, {error}')

	async def cog_before_invoke(self, ctx):
		self.bot.lj.log(f'emperor.cogs.api.{ctx.invoked_with}',
						f'{ctx.author.name} has attempted to executed {ctx.invoked_with}')

	async def cog_after_invoke(self, ctx):
		self.bot.lj.log(f'emperor.cogs.api.{ctx.invoked_with}',
						f'{ctx.author.name} has executed {ctx.invoked_with} command')

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
		async with aiohttp.ClientSession() as cs:
			async with cs.get(f'https://duckduckgo.com/html/?q={query}') as r:
				data = await r.text()

		# Parse the response data using BeautifulSoup
		soup = BeautifulSoup(data, 'html.parser')

		# Find all the search result links
		result_links = soup.select("a.result__a")

		# Extract the link and title for each result
		results = [(link['href'], link.text) for link in result_links]

		return results

	@app_commands.command(name="reddit", description="Looks through subreddits given by the user")
	async def reddit(
			self, interaction: discord.Interaction, subreddit: str
	):
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
		async with aiohttp.ClientSession() as cs:
			async with cs.get(subreddit_link) as r:

				# Convert to json
				json_data = await r.json()

				# Checking if the subreddit does exist
				if "error" in json_data:
					await interaction.response.send_message(
						"The subreddit does not exist, or has no content."
					)
					return

				post_data = json_data["data"]["children"][random.randint(0, len(json_data["data"]["children"]))]

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
					color=9240816,
				)
				post_embed.set_footer(
					text=f"👍 {post_data['data']['ups']} | 💬 {post_data['data']['num_comments']}"
				)
				post_embed.set_image(url=post_data["data"]["url"])
				# postEmbed.set_author(name=data['data']['author'])

				await interaction.response.send_message(embed=post_embed)

	@app_commands.command(name="ddg", description="Get search results from DuckDuckGo search")
	async def ddg_search(
			self, interaction: discord.Interaction, search_parameters: str
	):
		"""
		Get search from DuckDuckGo.
		Params:
			search_parameters: get search result from DuckDuckGo.
		"""
		results = await self.__get_search_results(search_parameters)

		resultEmbed = discord.Embed(color=self.bot.config.COLOUR, title="DDG search results")

		desc = ""

		resultLimit = 10

		for result in results:
			if resultLimit > 0:
				print(result[0])
				desc += f'[{result[1]}](https:{result[0]})\n'
				resultLimit -= 1

		resultEmbed.description = desc

		await interaction.response.send_message(embed=resultEmbed)

	
	
	# Create a GPT model

	# Define a function to generate text using the GPT model
	async def generate_text(self, prompt) -> str:
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
		else:
			# Send a default message if the response is empty
			return "I'm sorry, I cannot generate a response for this prompt."


	@app_commands.command(name="gpt", description="Generates text using a GPT model")
	@app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
	async def gpt(self, interactions: discord.Interaction, prompt: str):
		# Generate text using the GPT model
		text = await self.generate_text(prompt)

		# Send the generated text as a message in the Discord channel
		await interactions.response.send_message(text)


async def setup(bot):
	# Make an discord.Object for each
	# guild in the list
	guild_objects: list(discord.Object) = []
	for guild in bot.config.GUILD_ID:
		guild_objects.append(discord.Object(id=guild))

	await bot.add_cog(API(bot), guilds=guild_objects)
