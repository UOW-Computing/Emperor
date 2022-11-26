from discord.ext import commands
from discord.commands import Option
from src.util import *
from src.lj import LJ
import time


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kick",
                            description="Kicks the mentioned user",
                            guild_ids=GUILD_ID)
    async def kick(self, ctx, user: Option(discord.Member, "Enter the user to kick",
                                           required=True),
                   reason: Option(str, "Enter the reason the user is being kicked for",
                                  required=True, default="No Reason was provided!")):

        if ctx.author.id == user.id:
            await ctx.response.send_message(
                'You cannot kick yourself, it is not possible. `;-;`', ephemeral=True)
            return None

        # get a list of perms the member has
        perms = ', '.join(
                perm for perm, value in ctx.author.guild_permissions if value)

        userPerms = ', '.join(
            perm for perm, value in user.guild_permissions if value)

        # make sure that the user has perms to kick
        if 'kick_member' not in perms:
            await ctx.response.send_message("You do not have permission to execute this command!", ephemeral=True)
            return None

        # if the user has any manage perms then they cannot be kicked
        if 'manage_guild' in userPerms or 'kick_member' in userPerms or 'ban_memeber' in userPerms:
            await ctx.response.send_message("This user cannot be kicked, as they have manage perms", ephemeral=True)
            return None

        await discord.Member.kick(self=user, reason=reason)

        await ctx.respond(f'<@{user.id}> has been kicked from the server!')

    @commands.slash_command(name="clear",
                            description="Clears message in the mentiond channel",
                            guild_ids=GUILD_ID)
    async def clear(self, ctx, message_limit: Option(int, "Enter the number of messages to delete",
                                                     required=True, default=100)):
        # Respond to the user
        await ctx.response.send_message(
            f'Executing command in <#{ctx.channel.id}>', ephemeral=True)

        if int(message_limit) > 100:
            await ctx.followup.send(
                'Message limit is `100`, deleting more than `100` messages can only be done executing the command multiple times.',
                ephemeral=True)
            return -1

        # Get the messages and turn into list
        messagelist = await ctx.channel.history(limit=int(message_limit)).flatten()

        # Delete the messages one by one
        for message in messagelist:
            await message.delete()

        # inform the user the command has been executed
        await ctx.followup.send(f'Command Executed!', ephemeral=True)

    @commands.slash_command(name="announce",
                            description="Makes an announcement post in given channel",
                            guild_ids=GUILD_ID)
    async def announce(self, ctx, title: Option(str, "Enter Title", required=False, default=''),
                       description: Option(str, "Enter the announcement", required=True, default='')):
        # ensure that the description has a value
        # and the length does not go above
        # 4096 characters
        if description == '':
            await ctx.response.send_message(
                f'Command `{ctx.command.name}` requires parameter `description` to be provided.', ephemeral=True)
            return -1
        elif len(description) >= 4096:
            await ctx.response.send_message(f'`description` must be 4096 or less in length.', ephemeral=True)
            return -1

            # make the embed
        embed = discord.Embed(title=title if title != '' else None,
                              description=description)
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.user.display_avatar)
        embed.set_footer(text=self.bot.user.name,
                         icon_url=self.bot.user.display_avatar)
        # send the embed
        await ctx.respond(embed=embed)

    @commands.slash_command(name="addrole",
                            description="Adds a role",
                            guild_ids=GUILD_ID)
    async def add_role(self, ctx, *, role_name: Option(str, "Enter role name", required=True, default=None)):
        # local vars used
        ROLE_ALREADY_EXISTS_FLAG = False
        ROLE_ID = 0
        member = ctx.author
        guild = ctx.guild
        # role name, needs to be passed as
        # param
        if not role_name:
            await ctx.respond(f'Command: `{ctx.command.name}` takes in a parameter, none was provided.', ephemeral=True)
            return -1
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
                       f'<@{member.id}> has created role {role_name}')
            else:
                LJ.LOG(
                    "admins/roleAdd", f'{member} attempted to create a role that already exists!')
                await ctx.respond(f'<@&{ROLE_ID}> already exists, cannot create duplicate roles.')

        else:
            await ctx.respond(f'Insufficient Perms, <@{member.id}>')


def setup(bot):
    bot.add_cog(Admin(bot))
