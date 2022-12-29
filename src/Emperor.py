import os
import discord

from discord.ext import commands
from src.config import Settings
from src.lj import Lj

__cogs__ = ["admins", "generals"]


class Emperor(commands.Bot):
	"""
	Main class of the Bot
	Inherits all the properties of commnads.Bot

	"""

	log: Lj = None
	config: Settings = None

	def __init__(self, config: Settings):
		"""
		Constructor class for Emperor

		Main Bot class initializeds as well
		"""

		# Setting the intents
		# of the bot
		intents = discord.Intents(
			messages=True, guilds=True, presences=True, members=True, message_content=True
		)

		# Initilises the Constructor
		# for Lj class
		self.log = Lj()
		self.config = config

		super().__init__(
			command_prefix=[self.config.BOT_PREFIX, "t"],
			description="Very Important Discord Bot.",
			intents=intents,
			status=discord.Status.dnd,
			activity=discord.Game(name="with myself!"),
		)

		self.load_extensions()
		

	def load_extensions(self):
		
		for cog in os.listdir("./cogs"):
			if cog.endswith(".py"):
				print(f"Loaded {cog}")
				self.load_extension(f"cogs.{cog[:-3]}")

	async def log_in_channel(self, message: discord.Message) -> None:
		if self.config.LOG_CHANNEL_ID is None:
			self.log.warn(
				"logger/LogChannel",
				"Log Channel ID is undefined, cannot log inside servers",
			)
		log_channel = await message.guild.fetch_channel(self.config.LOG_CHANNEL_ID)

		# form a embed
		log_embed = discord.Embed(
			title="Content",
			description=f"{message.content}",
			timestamp=message.created_at,
			color=discord.Color.from_rgb(128, 0, 128),
		)
		log_embed.set_author(name=self.user.name, icon_url=self.user.display_avatar)
		log_embed.set_thumbnail(url=message.author.display_avatar)
		log_embed.add_field(
			name="Send by", value=f"<@{message.author.id}>", inline=True
		)
		log_embed.add_field(
			name="IDs",
			value=f"```\nMessage:\t{message.id}\nUser:\t{message.author.id}```",
			inline=True,
		)
		log_embed.add_field(
			name="Channel", value=f"<#{message.channel.id}>\nID: `{message.channel.id}`"
		)

		await log_channel.send(embed=log_embed)

	@commands.Cog.listener()
	async def on_ready(self):

		print(f"{self.user} is ready in {len(self.guilds)} servers!")

	@commands.Cog.listener()
	async def on_message(self, message):
		"""
		Handles all the messages sent by users

		Params:
						message: discord.Message, the event that triggered this function

		"""
		if message.author.bot:
			return None

		# Figure out if the message is from DM or guild
		await self.log_in_channel(message=message)
		self.log.log(
			f"{message.guild.name}/{message.channel.name}",
			f"{message.author} [MSG ID: {message.id}] {message.content}",
		)
		await self.process_commands(message)

	@commands.Cog.listener()
	async def on_command(self, ctx):
		self.log.log("main/CommandHandler", f"Executing {ctx.command}")
  
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		self.log.error('ErrorHandler', error)
		await ctx.channel.send(f"<@{ctx.author.id}> An error has occured!\n`{error}`")

