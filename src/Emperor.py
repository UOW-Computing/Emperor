"""
Emperor v0.1.2
	Main class


"""

import discord

from src.Lj import Lj
from src.config import Settings
from discord.ext import commands

class Emperor(commands.Bot):

	config: Settings = None
	lj: Lj = None

	def __init__(self, p_intents: discord.Intents, p_config: Settings) -> None:
		super().__init__(
				description="Very important discord bot",
				command_prefix=commands.when_mentioned_or('em!'),
				intents=p_intents)

		self.config = p_config	
		self.lj = Lj()

  
	async def setup_hook(self):
		for cog in self.config.COGS:
			try:
				await self.load_extension("cogs."+cog)
			except Exception as exc:
				print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')
	
	
	async def on_ready(self):
		self.lj.info('emperor.onready', f'Logged on as {self.user} (ID: {self.user.id})')

	async def on_message(self, message: discord.Message):

		if message.author.bot: return

		def check_for_message(msg: discord.Message):
			"""
			Insures that if an attachment is given the content is not left blank

			TODO: Add support to allow both content and attachments to be parsered through
			NOTE: Currently bugged, does not work with attachments
   
   	
			Args:
				msg (discord.Message): The message to parser through

			Returns:
				str: Message content if it had text
				url: Url(s) if the message had no content
			"""
			if message.content == "":
				return " ".join(message.attachments.url)
			else:
				return message.content

		

		self.lj.info(f'emperor.message    {message.guild.name}.{message.channel.name}', f'{message.author}: {message.content}')
		await self.process_commands(message)
  
  


