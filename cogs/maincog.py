import discord
import asyncio

from discord 		import app_commands
from discord.ext 	import commands


class Main(commands.Cog):
	"""The description for NewCog goes here."""

	def __init__(self, bot):
		self.bot = bot

	info_group = app_commands.Group(name="info", description="Gives information about server, member or channel.")

	async def cog_load(self):
		self.bot.lj.log('emperor.cogs.maincog', 'MainCog was loaded')

	async def cog_unload(self):
		# clean up logic goes here
		pass

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
		print(error)

	async def cog_before_invoke(self, ctx):
		print("Command is invoked")

	async def cog_after_invoke(self, ctx):
		print("Command was invoked")

	@app_commands.command(name="hello")
	async def hello(self, interaction: discord.Interaction) -> None:
		"""
		A simple hello command.

		Params:
			interaction: the event that causes this command to execute

		Returns
			Nothing
		"""
		await interaction.response.send_message(f"<@{interaction.user.id}>, helo!")

	# TODO: Complete the commands below
 
	@info_group.command(name='server')
	async def info_server(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message('This is a `/info server`')

	@info_group.command(name='member')
	async def info_member(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message('This is a `/info member`')

	@info_group.command(name='channel')
	async def info_channel(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message('This is a `/info channel`')

async def setup(bot):
	await bot.add_cog(Main(bot), guild=(discord.Object(id=bot.config.GUILD_ID)))
