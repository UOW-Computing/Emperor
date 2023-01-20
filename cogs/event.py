import re
import discord

from discord.ext import commands
from discord import RawReactionActionEvent
from src.ServerUtils import Utils

class NewCog(commands.Cog):
	"""The description for NewCog goes here."""

	def __init__(self, bot):
		self.bot = bot

	async def cog_load(self):
		self.bot.lj.log("emperor.cogs.event", "Event cog was loaded")

	async def cog_unload(self):
		self.bot.lj.warn("emperor.cogs.event", "Event cog was unloaded")


	async def on_error(self, event, *args, **kwargs):
		print(event)

	async def cog_before_invoke(self, ctx):
		# called before a command is called here
		pass

	async def cog_after_invoke(self, ctx):
		# called after a command is called here
		pass
	
 
	async def process_reaction(self, payload: RawReactionActionEvent, r_type=None) -> None:
		"""Process the reaction, decides to add or remove a role if it is a reaction message

		Args:
			payload (RawReactionActionEvent): The event that called the function
			r_type (_type_, optional): What to do with the role (add or remove). Defaults to None.
		"""

		self.bot.lj.log("emperor.cogs.event.process_reaction","Processing a reaction")		
  
		reaction_roles = Utils.read_from_json("res/reaction_roles.json")

		guild = self.bot.get_guild(payload.guild_id)			
		user = await guild.fetch_member(payload.user_id)

		# If the bot was the one to 
  		# react then do nothing
		if user.bot: return

		if str(payload.guild_id) in reaction_roles.keys():
			if str(payload.message_id) in reaction_roles[str(payload.guild_id)]:
				if user is None:
					self.bot.lj.warn("emperor.cogs.event.process_reaction", "User is None")
					return

				# Check if the emoji that was reacted 
				# is unicode
				if payload.emoji.is_unicode_emoji():
					role = \
		 		guild.get_role(reaction_roles[str(payload.guild_id)][str(payload.message_id)][str(payload.emoji.name)])
				else:
					role = \
		 		guild.get_role(reaction_roles[str(payload.guild_id)][str(payload.message_id)][str(payload.emoji.id)])
				
				# What happens if the role could not be found
				if role is None:
					self.bot.lj.warn("emperor.cogs.event.process_reaction",
f"An invalid role ID was provided in `reaction_roles` for message with ID: {payload.message_id}")

				# Add the role
				elif r_type == "add":

					self.bot.lj.log(
		 				"emperor.cogs.event.process_reaction",
					 	f"Role: {role.name} has been removed from {user.name}"
					 )

					await user.add_roles(role)

				# Remove the role
				elif r_type == "remove":
		
					self.bot.lj.log(
		 					"emperor.cogs.event.process_reaction",
					 		f"Role: {role.name} has been removed from {user.name}"
					 )
		
					await user.remove_roles(role)
				else:
					self.bot.lj.warn("emperor.cogs.event", "Invalid reaction type was provided in `process_reaction`.")


	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
		"""
		Whenever a reaction was added into a message, its called
		"""

		await self.process_reaction(payload, "add")

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
		"""
		Whenever a reaction was removed into a message, its called
		"""
		await self.process_reaction(payload, "remove")

async def setup(bot):
	await bot.add_cog(NewCog(bot))
