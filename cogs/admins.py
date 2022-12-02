# pylint: disable=no-else-return
"""
admins.py

Holds all the commands for admin category.
"""

import discord

from discord.commands import Option
from discord.ext import commands

from src.util import GUILD_ID
from src.lj import LJ


class Admin(commands.Cog):
    """
    Admin category for Emperor.

    Contains the following commands:
    - announce
    - kick
    - clear
    - createrole 
    // TODO: CHANGE COMMAND NAME INTO CREATE, add subcommands ROLE/CHANNEL

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kick",
                            description="Kicks the mentioned user",
                            guild_ids=GUILD_ID)
    async def kick(self, ctx,
                   user: Option(discord.Member,
                            "Enter the user to kick",
                            required=True),
                   reason: Option(str,
                            "Enter the reason the user is being kicked for",
                            required=True, default="No Reason was provided!")):
        """
        Command to kick a user from the server.

        Args:
            ctx: The context of the command
            user: The person to kick
            reason: Why is the user getting kicked

        Returns:
            None: The user did not have permission or usage was incorrect
            Nothing: The command was executed correctly
        """

        if ctx.author.id == user.id:
            await ctx.response.send_message(
                'You cannot kick yourself, it is not possible. `;-;`',
                ephemeral=True)
            LJ.LOG("admins/kick",
                   "User attempted to kick themselves, stopped execution.")
            return None

        # get a list of perms the member has
        perms = ', '.join(
                perm for perm, value in ctx.author.guild_permissions if value)

        userPerms = ', '.join(
            perm for perm, value in user.guild_permissions if value)

        # make sure that the user has perms to kick
        if 'kick_member' not in perms:
            await ctx.response.send_message(
                "You do not have permission to execute this command!",
                ephemeral=True)
            LJ.LOG("admins/kick",
                   "User has no perms to run this command, stopped execution.")
            return None

        # if the user has any manage perms then they cannot be kicked
        match(userPerms):
            case 'kick_member':
                await ctx.response.send_message("This user cannot be kicked!",
                                                ephemeral=True)
                LJ.LOG("admins/kick",
                       "User could not be kicked, stopping execution.")
                return None

        await discord.Member.kick(self=user, reason=reason)
        LJ.LOG("admins/kick", f'{user} has been kicked by {ctx.author}')
        await ctx.respond(f'<@{user.id}> has been kicked from the server!')

    @commands.slash_command(name="clear",
                            description="Deletes messages in a channel",
                            guild_ids=GUILD_ID)
    async def clear(self, ctx,
                    mlimit: Option(int,
                        "Enter the number of messages to delete",
                        required=True, default=100)):

        """
        Clears a channels messages

        Args:
            mlimit: the number of messages to delete (default is 100)

        Returns:
            None: Indicating that the command run unsuccessfuly
            Nothing: The cccommand run successful.

        """
        # Respond to the user
        await ctx.response.send_message(
            f'Executing command in <#{ctx.channel.id}>', ephemeral=True)

        if int(mlimit) > 100:
            await ctx.followup.send("""Message limit is `100`.
            Deleting `>100` messages cannot be done through a single command.
            Use the command multiple times to delete more than 100 messages.
            """,
                                    ephemeral=True)
            LJ.LOG("admins/clear",
                   "Command stopped due to message limit being >100.")
            return -1

        # get a list of perms the member has
        perms = ', '.join(
                perm for perm, value in ctx.author.guild_permissions if value)

        if 'manage_messages' in perms:
            # Respond to the user
            await ctx.response.send_message(
                f'Executing command in <#{ctx.channel.id}>', ephemeral=True)

            # Get the messages and turn into list
            messagelist = await ctx.channel.history(limit=mlimit).flatten()

            # Delete the messages one by one
            for message in messagelist:
                await message.delete()

            LJ.LOG("admins/clear",
                f"Cleared {mlimit} messages in <#{ctx.channel.id}>")

            # inform the user the command has been executed
            await ctx.followup.send('Command Executed!', ephemeral=True)
        else:
            await ctx.response.send_message('You do not have perms for this!!', 
            ephemeral=True)

    @commands.slash_command(name="announce",
                            description="Sends a embed in given channel",
                            guild_ids=GUILD_ID)
    async def announce(self, ctx,
                       title: Option(str,
                            "Enter Title", required=False, default=''),
                       description: Option(str,
                            "Enter the announcement", required=True, default='')
                       ):
        """
        Makes an embed in the mentioned channel

        Args:
            title: the title of the embed
            description: the description of the embedd (the content)

        Returns:
            None: Indicating that the command run unsuccessfuly
            Nothing: The command run successful.

        """
        # ensure that the description has a value
        # and the length does not go above
        # 4096 characters
        if description == '':
            await ctx.response.send_message(
                f'`{ctx.command.name}` requires `description` to be given.',
                ephemeral=True)
            LJ.LOG("admins/announce",
                   message='Parameter was not given, stopping execution.')
            return -1
        elif len(description) >= 4096:
            await ctx.response.send_message(
                '`description` must be 4096 or less in length.', ephemeral=True)
            LJ.LOG("admins/announce",
                   'Parameter size is >4096 characters, stopping execution.')
            return -1

        # make the embed
        embed = discord.Embed(title=title if title != '' else None,
                              description=description)
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.user.display_avatar)
        embed.set_footer(text=self.bot.user.name,
                         icon_url=self.bot.user.display_avatar)

        LJ.LOG(context="admins/announce",
            message=f"announce executed by {ctx.author} in <#{ctx.channel.id}>")
        # send the embed
        await ctx.respond(embed=embed)

    @commands.slash_command(name="createrole",
                            description="Adds a role",
                            guild_ids=GUILD_ID)
    async def create_role(self, ctx, *,
                       role_name: Option(str,
                                         "Enter role name",
                                         required=True, default=None)):
        """
        Creates a new role

        Args:
            role_name: The name of the role

        Returns:
            None: Indicating that the command run unsuccessfuly
            Nothing: The command run successful.

        """
        # local vars used
        ROLE_ALREADY_EXISTS_FLAG = False
        ROLE_ID = 0
        member = ctx.author
        guild = ctx.guild
        # role name, needs to be passed as
        # param
        if not role_name:
            await ctx.respond(
                f'`{ctx.command.name}` takes a parameter, none was provided.',
                ephemeral=True)
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

            if ROLE_ALREADY_EXISTS_FLAG is False:
                await guild.create_role(
                    name=role_name,
                    reason=f'{member} created role through command')
                LJ.LOG("admins/roleAdd",
                       f'<@{member.id}> has created role {role_name}')
            else:
                LJ.LOG("admins/roleAdd",
                       f'{member} attempted to create a role that already exists!')
                await ctx.respond(
                    f'<@&{ROLE_ID}> exists, cannot create duplicate roles.')

        else:
            await ctx.respond(f'Insufficient Perms, <@{member.id}>')


def setup(bot):
    bot.add_cog(Admin(bot))
