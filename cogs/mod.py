import discord
import asyncio

from datetime import datetime
from discord.ext import commands
from discord import app_commands


class Mod(commands.Cog):
	"""
	Moderation cog

	Holds all the commands for moderation
	"""

	ticket_number = 0

	def __init__(self, bot):
		self.bot = bot

	ticket_group = app_commands.Group(
		name="ticket", description="Creates tickets for supports"
	)

	async def cog_load(self):
		self.bot.lj.log("emperor.cogs.mod", "Moderation cog was loaded")

	async def cog_unload(self):
		self.bot.lj.warn("emperor.cogs.mod", "Moderation cog was unloaded")

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
		# Checks if the command is on cooldown,
		# if so tell the user
		if isinstance(error, app_commands.CommandOnCooldown):
			on_cooldown: str = f"You are currently on cooldown, try again in <t:{int(datetime.now().timestamp()+error.retry_after)}:R>."
			await interaction.response.send_message(
				on_cooldown, delete_after=error.retry_after
			)

		self.bot.lj.warn(
			f"emperor.cogs.mod.{interaction.command.name}",
			f"<@{interaction.user.id}>, {error}",
		)

		# Handles the InteractionAlreadyBeenResponsed to Exception
		try:
			await interaction.response.send_message(
				f"<@{interaction.user.id}>, {error}"
			)
		except:
			self.bot.lj.warn(
				f"emperor.cogs.mod.{interaction.command.name}",
				f"<@{interaction.user.id}>, {error}",
			)

	async def cog_before_invoke(self, ctx):
		self.bot.lj.log(
			f"emperor.cogs.mod.{ctx.invoked_with}",
			f"{ctx.author.name} has attempted to executed {ctx.invoked_with}",
		)

	async def cog_after_invoke(self, ctx):
		self.bot.lj.log(
			f"emperor.cogs.mod.{ctx.invoked_with}",
			f"{ctx.author.name} has executed {ctx.invoked_with} command",
		)

	@app_commands.command(name="hellomod", description="Sends hello to mod")
	@app_commands.checks.has_permissions(moderate_members=True)
	async def hellomod(self, i: discord.Interaction):
		await i.response.send_message("Hello, mod!")


	@app_commands.command(name="purge", description="Purges the channel of messages")
	@app_commands.checks.has_permissions(manage_messages=True)
	async def purge(self, interaction: discord.Interaction, limit: int = 100) -> None:
		"""Removes a x ammount of messages in a executed channel.

		Args:
			limit (int, optional): The number of messages to delete. Defaults to 100.
		"""
		# Removes {limit} amount of messages in a channel 
		await interaction.response.defer()
		await interaction.channel.purge(limit=limit, before=interaction.created_at)
		# informs the user that the channel has been purged
		await interaction.followup.send(f'Purged {limit} messages by {interaction.user.name}')


	# Ticket commands below #
	@ticket_group.command(
		name="create", description="Creates a channel for the ticket to be handled"
	)
	@app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
	async def ticket_create(
		self, interaction: discord.Interaction, reason: str
	) -> None:
		"""
		Creates a channel for the ticket to be handled by support

		Args:
				reason (str): The purpose of the ticket being open
		"""

		role = interaction.guild.get_role(
			int(self.bot.config.STAFF_IDS[str(interaction.guild.id)])
		)  # self.bot.config.SUPPORT_ROLE
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(
				read_messages=False
			),
			interaction.user: discord.PermissionOverwrite(read_messages=True),
			role: discord.PermissionOverwrite(read_messages=True),
		}

		guild = interaction.guild

		self.ticket_number += 1
		channel_name = f"ticket-{self.ticket_number:02}"
		channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

		supportEmbed = discord.Embed(
			color=self.bot.config.COLOUR,
			title="Support Ticket",
			description="Thank you for creating a support ticket, any moment staff members will get in touch!",
		)

		supportEmbed.add_field(name="Reason for ticket", value=reason)

		await channel.send(embed=supportEmbed)

		self.bot.lj.log(
			"emperor.mod.ticket.create",
			f"Ticket ({channel.id}) has been created by {interaction.user.name}",
		)

		await interaction.response.send_message(
			f"Ticket has been created, <#{channel.id}>"
		)

	@ticket_group.command(name="close", description="Closes an already open ticket")
	async def ticket_close(self, interaction: discord.Interaction) -> None:
		"""
		Closes an already open ticket made by an member

		Args:
				None (user side)
		"""
		# Check if the channel is ticket channel
		guild = interaction.guild

		channel = guild.get_channel(interaction.channel_id)

		thankEmbed = discord.Embed(
			color=self.bot.config.COLOUR,
			description="Hope your issue was resolved, the ticket has now been closed.",
		)

		is_ticket_channel: bool = channel.name.startswith("ticket")

		if is_ticket_channel:
			await interaction.response.send_message(embed=thankEmbed)
			self.bot.lj.log(
				"emperor.mod.ticket.close",
				f"Ticket ({channel.id}) has been closed by {interaction.user.name}",
			)
			await asyncio.sleep(5)
			await channel.delete()
		else:
			await interaction.response.send_message(
				"This command cannot be used outside of a ticket!"
			)


async def setup(bot):
	# Make an discord.Object for each
	# guild in the list
	guild_objects: list(discord.Object) = []
	for guild in bot.config.GUILD_ID:
		guild_objects.append(discord.Object(id=guild))

	await bot.add_cog(Mod(bot), guilds=(guild_objects))
