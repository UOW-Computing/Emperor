import discord
import asyncio

from discord 		import app_commands
from discord.ext 	import commands

class Admin(commands.Cog):
	"""The description for NewCog goes here."""

	def __init__(self, bot):
		self.bot = bot

	async def cog_load(self):
		self.bot.lj.info('emperor.cogs.admin', 'Admin cog was loaded')

	async def cog_unload(self):
		self.bot.lj.warn('emperor.cogs.admin', 'Admin cog was unloaded')

	async def cog_check(self, ctx):
		return await self.bot.is_owner(ctx.author)


	async def bot_check(self, ctx):
		# checks that apply to every command to the bot
		return True

	async def bot_check_once(self, ctx):
		# check that apply to every command but is guaranteed to be called only once
		return True

	async def cog_command_error(self, ctx, error):
		print(error)
		
	async def cog_app_command_error(self, interaction, error):
		self.bot.lj.warn(f'emperor.cogs.admin.{interaction.command.name}',
				   		 f'<@{interaction.user.id}>, {error}')
		await interaction.response.send_message(f'<@{interaction.user.id}>, {error}')

	async def cog_before_invoke(self, ctx):
		self.bot.lj.info(f'emperor.cogs.admin.{ctx.invoked_with}',
					f'{ctx.author.name} has attempted to executed {ctx.invoked_with}')

	async def cog_after_invoke(self, ctx):
		self.bot.lj.info(f'emperor.cogs.admin.{ctx.invoked_with}',
					f'{ctx.author.name} has executed {ctx.invoked_with} command')

	@commands.command(name="reload")
	async def reload(self, ctx: commands.Context, cog: str) -> None:
		"""
		Allows the changes to be run without having the restart the discord bot

		Args:
			cog str: The cog to reload


		"""

		try:
			await self.bot.unload_extension('cogs.'+cog)
			await self.bot.load_extension('cogs.'+cog)
			
			# The cog was reloaded
			await ctx.send(f'The `{cog}` was successfully reloaded')
		except Exception as exc:
			await ctx.send(exc)

async def setup(bot):
	# Make an discord.Object for each
	# guild in the list
	guild_objects: list(discord.Object) = []
	for guild in bot.config.GUILD_ID:
		guild_objects.append(discord.Object(id=guild))

	await bot.add_cog(Admin(bot), 	guilds=guild_objects)
