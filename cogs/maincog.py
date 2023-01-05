import discord

import asyncio

from discord 		import app_commands
from discord.ext 	import commands
from datetime		import datetime as dt
from discord.utils	import format_dt


class Main(commands.Cog):
	"""
 	Main Cog

	Holds all the commands that do not fit a specific catagory
	"""

	def __init__(self, bot):
		self.bot = bot

	info_group = app_commands.Group(name="info", description="Gives information about server, member or channel.")

	async def cog_load(self):
		self.bot.lj.info('emperor.cogs.maincog', 'MainCog cog was loaded')

	async def cog_unload(self):
		self.bot.lj.warn('emperor.cogs.maincog', 'MainCog cog was unloaded')

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
		self.bot.lj.warn(f'emperor.cogs.maincog.{interaction.command.name}',
				   		 f'<@{interaction.user.id}>, {error}')
		await interaction.response.send_message(f'<@{interaction.user.id}>, {error}')

	async def cog_before_invoke(self, ctx):
		self.bot.lj.info(f'emperor.cogs.maincog.{ctx.invoked_with}',
						 f'{ctx.author.name} has attempted to executed {ctx.invoked_with}')

	async def cog_after_invoke(self, ctx):
		self.bot.lj.info(f'emperor.cogs.maincog.{ctx.invoked_with}',
						 f'{ctx.author.name} has executed {ctx.invoked_with} command')


	async def __count_online_members(self, guild: discord.Guild) -> int:
		"""Counts the number of online members in the guild

		Args:
			guild (discord.Guild): The guild to get the members from

		Returns:
			int: The number of online (online & dnd) members
		"""
		num = 0
		for member in guild.members:
			if member.status == discord.Status.dnd or\
       		   member.status == discord.Status.do_not_disturb or\
               member.status == discord.Status.online:
				num += 1
	
		return num

	def __count_bot(self, guild: discord.Guild) -> int:
		"""Counts the number of bots in the guild

		Args:
			guild (discord.Guild): The guild to count the bots from

		Returns:
			int: The number of bots in the guild
		"""
		num = 0
		for member in guild.members:
			if member.bot:
				num += 1

		return num

	def __count_top_three_roles(self, member: discord.Member) -> str:
		roles = ""
    
		roles += f"<@&{member.roles[-1].id}>, "
		roles += f"<@&{member.roles[-2].id}>, "
		roles += f"<@&{member.roles[-3].id}>."

		return roles

	def __count_emojis(self, guild: discord.Guild) -> str:
		"""
		Counts the number of emojis in the server

		Args:
			guild (discord.Guild): The guild to count the emojis from

		Returns:
			str: The emojis as <:emoji_name:emoji_id> or
				 the string number of emojis
		"""
		if len(guild.emojis) == 0:
			return "0"
		emojilist = " ".join([f'<:{emoji.name}:{emoji.id}>' for emoji in guild.emojis])
		if len(emojilist) >= 1024:
			return str(len(guild.emojis))
		else:
			return emojilist


	@app_commands.command(name="hello")
	async def hello(self, interaction: discord.Interaction) -> None:
		"""
		A simple hello command.

		Params:
			interaction: the event that causes this command to execute

		Returns
			Nothing
		"""
		await interaction.response.send_message(f"<@{interaction.user.id}>, hello!")


	@info_group.command(name='server')
	async def info_server(self, interaction: discord.Interaction) -> None:
		"""Collects and sends an embed with information about the server

		Args:
			interaction (discord.Interaction): The trigger for this command

		Returns:
			Embed (discord.Embed): Contains the information gathered on 
			the guild
		"""
		
		discordfile = None
		guild = interaction.guild
		if guild.icon is None:
			discordfile = discord.File("res/discordLogo.png", filename="logo.png")

		server_embed = discord.Embed(color=self.bot.config.COLOUR ,title=guild.name, description=guild.description)
		img_url = guild.icon if guild.icon is not None else "attachment://logo.png"
		server_embed.set_thumbnail(url=img_url)
		server_embed.add_field(name="Owner", value=f"<@{guild.owner_id}>", inline=True)

		if guild.banner:
			server_embed.set_image(url=guild.banner.url)

		# Display the total member count with online and offline
		server_embed.add_field(name="Members",
						 		value=f'{guild.member_count} ({await self.__count_online_members(guild)} online)',
						   		inline=True)

		# Get the number of bots in the server
		server_embed.add_field(name="Bots",
							   value=self.__count_bot(guild),
							   inline=True)

		# Get the roles and make them mentionable
		server_embed.add_field(name="Roles",
		                  	   value= len(guild.roles),
                        	   inline=True)

		server_embed.add_field(name="Channels",
                         	   value=len(guild.channels),
                               inline=True)
  
		server_embed.add_field(name="Emojis",
                         	   value=self.__count_emojis(guild),
                               inline=True)

		server_embed.set_footer(text=f'ID: {guild.id} | Server Created • {(guild.created_at.strftime("%Y/%m/%d %H:%M %p"))}')

		if guild.icon is not None:
			await interaction.response.send_message(embed=server_embed)
		else:
			await interaction.response.send_message(file=discordfile, embed=server_embed)
		# await interaction.response.send_message('This is a `/info server`')

	@info_group.command(name='member')
	async def info_member(self, interaction: discord.Interaction, member: discord.Member) -> None:
		memberEmbed = discord.Embed(color=self.bot.config.COLOUR,
                              		title='Member Information',
                                	description=\
            f"""Name: `{member.name}{f" ({member.display_name})" if member.display_name != member.name else ""}`
            Joined Discord on: {format_dt(member.created_at)}
            Joined Server on: {format_dt(member.joined_at)}
            Roles: {self.__count_top_three_roles(member)}""")

		memberEmbed.set_image(url=member.display_avatar.url)
		memberEmbed.set_footer(text=f'{self.bot.user.name} | {dt.now().strftime("%d %B %Y %H:%M %p")}',
                         	   icon_url=self.bot.user.display_avatar)
  
		await interaction.response.send_message(embed=memberEmbed)

async def setup(bot):
	# Make an discord.Object for each
	# guild in the list
	guild_objects: list(discord.Object) = []
	for guild in bot.config.GUILD_ID:
		guild_objects.append(discord.Object(id=guild))

	await bot.add_cog(Main(bot), guilds=guild_objects)
