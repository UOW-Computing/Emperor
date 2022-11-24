from discord.ext import commands
from src.util import *
from src.lj import LJ


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #

    @commands.slash_command(name="addrole", description="Adds a role", guild_ids=[573602053352456193])
    async def add_role(self, ctx, *, role_name=None):
        # local vars used
        ROLE_ALREADY_EXISTS_FLAG = False
        ROLE_ID = 0
        member = ctx.author
        guild = ctx.guild
        # role name, needs to be passed as
        # param
        if not role_name:
            await ctx.send(embed=no_args_erro(ctx.author, ctx.command.name))
        # get a list of perms the member has
        perms = ', '.join(
            perm for perm, value in member.guild_permissions if value)

        # does the user have perms to make role
        if 'manage_roles' in perms:
            # check if the role already exists
            roles = await guild.fetch_roles()
            for role in roles:
                if role.name == role_name:
                    # print("Role already exists")
                    ROLE_ALREADY_EXISTS_FLAG = True
                    ROLE_ID = role.id
                    break

            if ROLE_ALREADY_EXISTS_FLAG == False:
                await guild.create_role(name=role_name, reason=f'{member} created role through command')
                LJ.LOG("admins/roleAdd",
                       f'{member} has created role {role_name}')
            else:
                LJ.LOG(
                    "admins/roleAdd", f'{member} attempted to create a role that already exists!')
                await ctx.respond(f'{member}, <@&{ROLE_ID}> already exists. Duplicate roles cannot be created!')

        else:
            await ctx.respond(f'Insufficient Perms, <@{member.id}>')


def setup(bot):
    bot.add_cog(Admin(bot))
