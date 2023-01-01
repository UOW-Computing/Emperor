"""
Emperor v0.1.0
	Main class


"""

import discord

from src.config import Settings
from discord.ext import commands
from src.Lj import Lj

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
		self.lj.log('emperor.onready', f'Logged on as {self.user} (ID: {self.user.id})')

	async def on_message(self, message: discord.Message):

		if message.author.bot: return

		self.lj.log(f'emperor.message    {message.guild.name}.{message.channel.name}', f'{message.author}: {message.content}')
		await self.process_commands(message)
  
  


