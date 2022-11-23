from discord.ext import commands
from util import *
from lj import LJ

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="addrole", aliases=['addRole', 'roleAdd', 'newRole', 'createRole'])
	async def add_role(self, ctx, *, args = None):
		# local vars used
		ROLE_ALREADY_EXISTS_FLAG = False
		ROLE_ID = 0
		member = ctx.author
		guild = ctx.guild

		# role name, needs to be passed as 
		# param		
		if not args:
			await ctx.send(embed=no_args_erro(ctx.author, ctx.command.name))
		# get a list of perms the member has
		perms = ', '.join(perm for perm, value in member.guild_permissions if value)
		
		# does the user have perms to make role 
		if 'manage_roles' in perms:
			# check if the role already exists
			roles = await guild.fetch_roles()
			for role in roles:
				if role.name == args:
					# print("Role already exists")
					ROLE_ALREADY_EXISTS_FLAG = True
					ROLE_ID = role.id
					break
			
			if ROLE_ALREADY_EXISTS_FLAG == False:
				await guild.create_role(name=args, reason=f'{member} created role through command')
				LJ.LOG("admins/roleAdd", f'{member} has created role {args}')
			else:
				LJ.LOG("admins/roleAdd", f'{member} attempted to create a role that already exists!')
				await ctx.send(f'{member}, <@&{ROLE_ID}> already exists. Duplicate roles cannot be created!')

		else:
			await ctx.send(f'Insufficient Perms, <@{member.id}>')
			


async def setup(bot):
	await bot.add_cog(Admin(bot))