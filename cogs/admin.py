import discord
import asyncio

from discord 		import app_commands
from discord.ext 	import commands

class Admin(commands.Cog):
	"""The description for NewCog goes here."""

	def __init__(self, bot):
		self.bot = bot

	async def cog_load(self):
		print("Loaded admin cog")

	async def cog_unload(self):
		# clean up logic goes here
		pass

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
		print(error)

	async def cog_before_invoke(self, ctx):
		print("Command is invoked")

	async def cog_after_invoke(self, ctx):
		print("Command was invoked")

	@commands.command(name="reload")
	async def reload(self, ctx: commands.Context, cog: str) -> None:
		"""
		Reload function
		"""

		try:
			await self.bot.unload_extension('cogs.'+cog)
			await self.bot.load_extension('cogs.'+cog)
			
			# The cog was reloaded
			await ctx.send(f'The `{cog}` was successfully reloaded')
		except Exception as exc:
			ctx.send(f"Cannot reload the cog, {exc}")

async def setup(bot):
	await bot.add_cog(Admin(bot), 	guild=(discord.Object(id=bot.config.GUILD_ID)))
