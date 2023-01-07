import os
import json
import discord


from discord.ext import commands

class MyHelpCommand(commands.HelpCommand):

	async def send_bot_help(self, mapping):
		embed = discord.Embed(title="Help", description="Use `em!help` for this embed again!")
		# Get help.json
		with open(os.path.realpath('res/help.json'), 'r') as helpJSON:
			data = json.loads(helpJSON.read())
		helpJSON.close()

		for cog in data:
			cog_commands = ""
			for command in data[cog]:	
				for i in range(len(data[cog][command])):
					cog_commands += f"`{data[cog][command][i]['usage']}`: {data[cog][command][i]['description']}\n"

			embed.add_field(name=cog,
							value=cog_commands,
							inline=True)

		channel = self.get_destination()
		await channel.send(embed=embed)


class Help(commands.Cog):
	def __init__(self, bot) -> None:
		self.bot = bot

		# Focus here
		# Setting the cog for the help
		help_command = MyHelpCommand()
		help_command.cog = self # Instance of YourCog class
		bot.help_command = help_command


async def setup(bot):
	await bot.add_cog(Help(bot))

async def teardown(bot):
	bot.help_command = bot._default_help_command
