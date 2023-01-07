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

	ticket_group = app_commands.Group(name="ticket", 
                                   	  description="Creates tickets for supports")

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


	@ticket_group.command(name="create",
						  description="Creates a channel for the ticket to be handled")
	async def ticket_create(self, interaction: discord.Interaction,  reason: str) -> None:
		
		role = interaction.guild.get_role(1045055491220443287) # self.bot.config.SUPPORT_ROLE
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
			interaction.user: discord.PermissionOverwrite(read_messages=True),
			role: discord.PermissionOverwrite(read_messages=True)
		}

		guild = interaction.guild

		channel = await guild.create_text_channel('ticket-00', overwrites=overwrites)

		supportEmbed = discord.Embed(color=self.bot.config.COLOUR, title="Support Ticket",
				description="Thank you for creating a support ticket, any moment staff members will get in touch!")

		supportEmbed.add_field(name='Reason for ticket',
							   value=reason)

		await channel.send(embed=supportEmbed)

		await interaction.response.send_message(f'Ticket has been created, <#{channel.id}>')
  
	@ticket_group.command(name="close",
						  description='Closes an already open ticket')
	async def ticket_close(self, interaction: discord.Interaction) -> None:
		# Check if the channel is ticket channel
		guild = interaction.guild

		channel = guild.get_channel(interaction.channel_id)

		thankEmbed = discord.Embed(color=self.bot.config.COLOUR,
								   description="Hope your issue was resolved, the ticket has now been closed.")

		is_ticket_channel: bool = channel.name.startswith('ticket')

		if is_ticket_channel:
			await interaction.response.send_message(embed=thankEmbed)
			await asyncio.sleep(5)
			await channel.delete()
		else:
			await interaction.response.send_message('This command cannot be used outside of a ticket!')
  


async def setup(bot):
    # Make an discord.Object for each
    # guild in the list
	guild_objects: list(discord.Object) = []
	for guild in bot.config.GUILD_ID:
		guild_objects.append(discord.Object(id=guild))

	await bot.add_cog(Mod(bot), guilds=(guild_objects))
