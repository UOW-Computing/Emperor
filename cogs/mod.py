import discord
import asyncio

from discord 		import app_commands
from discord.ext 	import commands

class Mod(commands.Cog):
	"""
	Moderation cog
	
	Holds all the commands for moderation
	"""

	def __init__(self, bot):
		self.bot = bot

	async def cog_load(self):
		self.bot.lj.info('emperor.cogs.mod', 'Moderation cog was loaded')

	async def cog_unload(self):
		self.bot.lj.warn('emperor.cogs.mod', 'Moderation cog was unloaded')

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
		self.bot.lj.warn(f'emperor.cogs.mod.{interaction.command.name}',
				   		 f'<@{interaction.user.id}>, {error}')
		await interaction.response.send_message(f'<@{interaction.user.id}>, {error}')

	

	async def cog_before_invoke(self, ctx):
		self.bot.lj.info(f'emperor.cogs.mod.{ctx.invoked_with}',
						 f'{ctx.author.name} has attempted to executed {ctx.invoked_with}')

	async def cog_after_invoke(self, ctx):
		self.bot.lj.info(f'emperor.cogs.mod.{ctx.invoked_with}',
						 f'{ctx.author.name} has executed {ctx.invoked_with} command')

	@app_commands.command(name='hellomod',
					   	  description='Sends hello to mod')
	@app_commands.checks.has_permissions(moderate_members=True)
	async def hellomod(self, i: discord.Interaction):
		await i.response.send_message('Hello, mod!')

async def setup(bot):
    # Make an discord.Object for each
    # guild in the list
	guild_objects: list(discord.Object) = []
	for guild in bot.config.GUILD_ID:
		guild_objects.append(discord.Object(id=guild))

	await bot.add_cog(Mod(bot), guilds=(guild_objects))
