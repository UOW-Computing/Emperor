from discord.ext import commands
from util import *
from lj import LJ

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="addrole", aliases=['addRole', 'roleAdd', 'newRole', 'createRole'])
	async def add_role(self, ctx, *, args = None):

		member = ctx.author
		guild = ctx.guild
		
		if not args:
			await ctx.send(embed=no_args_erro(ctx.author, ctx.command.name))
		# get a list of perms the member has
		perms = ', '.join(perm for perm, value in member.guild_permissions if value)

		if 'manage_roles' in perms:
			await guild.create_role(name=args, reason=f'{member} created role through command')
			LJ.LOG("admins/roleAdd", f'{member} has created role {args}')
			


async def setup(bot):
	await bot.add_cog(Admin(bot))