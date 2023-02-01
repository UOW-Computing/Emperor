"""
Emperor, discord bot for school of computing
Copyright (C) 2022-2023  School of Computing Dev Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import re
import json
import asyncio
import discord

from datetime import datetime
from typing import Optional
from discord.ext import commands
from discord import app_commands
from src.ServerUtils import Utils


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

    reaction_group = app_commands.Group(
        name="reactionrole", description="Links a role to a reaction in a message"
    )

    create_group = app_commands.Group(
        name="create", description="Set of create commands."
    )

    async def cog_load(self):
        self.bot.lj.log("emperor.cogs.mod", "Moderation cog was loaded")

    async def cog_unload(self):
        self.bot.lj.warn("emperor.cogs.mod", "Moderation cog was unloaded")

    async def cog_app_command_error(self, interaction, error):

        self.bot.lj.warn(
            f"emperor.cogs.mod.{interaction.command.name}",
            f"<@{interaction.user.id}>, {error}",
        )

        # Checks if the command is on cooldown,
        # if so tell the user
        if isinstance(error, app_commands.CommandOnCooldown):
            on_cooldown: str = f"You are currently on cooldown, try again in <t:{int(datetime.now().timestamp()+error.retry_after)}:R>."
            await interaction.response.send_message(
                on_cooldown, delete_after=error.retry_after, ephemeral=True
            )
            return

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

    @app_commands.command(name="purge", description="Purges the channel of messages")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, limit: int = 100) -> None:
        """Removes a x ammount of messages in a executed channel.

        Args:
            limit (int, optional): The number of messages to delete. Defaults to 100.
        """

        if limit > 100:
            await interaction.response.send_message(
                "Please purge messages in 100 increments.", ephemeral=True
            )
            return

        # Gives us 15 mins of time to respond
        await interaction.response.defer()

        # Purges all the message till the limit
        # leaves the interaction that called it
        await interaction.channel.purge(limit=limit, before=interaction.created_at)

        # informs the user that the channel has been purged
        await interaction.followup.send(
            f"Purged `{limit}` messages by {interaction.user.name}"
        )

    # Ticket commands below #
    @ticket_group.command(
        name="new", description="Creates a channel for the ticket to be handled"
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

        # Gets the Guild
        guild = interaction.guild

        # Gets the @Staff role for the guild
        role = guild.get_role(
            int(self.bot.config.STAFF_IDS[str(interaction.guild.id)])
        )  # self.bot.config.SUPPORT_ROLE
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }

        # Ticket channel name
        self.ticket_number += 1
        channel_name = f"ticket-{self.ticket_number:02}"

        # Create the channel with the ticket
        # channel name above
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

        # Make the embed
        support_embed = discord.Embed(
            color=self.bot.config.COLOUR,
            title="Support Ticket",
            description="Thank you for creating a support ticket, any moment staff members will get in touch!",
        )

        support_embed.add_field(name="Reason for ticket", value=reason)

        # Send the embed in the ticket
        # just created
        await channel.send(embed=support_embed)

        self.bot.lj.log(
            "emperor.mod.ticket.create",
            f"Ticket ({channel.id}) has been created by {interaction.user.name}",
        )

        # Inform the user the channel ticket has been
        # created
        await interaction.response.send_message(
            f"Ticket has been created, <#{channel.id}>", ephemeral=True
        )

    @ticket_group.command(name="close", description="Closes an already open ticket")
    async def ticket_close(self, interaction: discord.Interaction) -> None:
        """
        Closes an already open ticket made by an member
        """
        # Check if the channel is ticket channel
        guild = interaction.guild

        # Get the channel
        channel = guild.get_channel(interaction.channel_id)

        # Create the closing embed
        response_embed = discord.Embed(
            color=self.bot.config.COLOUR,
            description="Hope your issue was resolved, the ticket has now been closed.",
        )

        # Check for if the channel is a
        # ticket channel
        is_ticket_channel: bool = channel.name.startswith("ticket")

        if is_ticket_channel:

            # Send the formailties
            # for closing the channel
            await interaction.response.send_message(embed=response_embed)
            self.bot.lj.log(
                "emperor.mod.ticket.close",
                f"Ticket ({channel.id}) has been closed by {interaction.user.name}",
            )

            # Let the user read then delete
            await asyncio.sleep(5)
            await channel.delete()
        else:
            await interaction.response.send_message(
                "This command cannot be used outside of a ticket!"
            )

    # Reaction role command
    @reaction_group.command(
        name="create",
        description="Links the message with the reactions that are linked with roles",
    )
    @app_commands.checks.has_permissions(manage_roles=True, manage_emojis=True)
    async def reaction_create(
        self,
        interaction: discord.Interaction,
        message_id: str,
        role: discord.Role,
        reaction: str,
    ) -> None:
        """
        Generates a binding in json file, allowing the event handler know its a reaction message

        Args:
            message_id (str): The message that needs to be a reaction message
            role (discord.Role): Role to add
            reaction (str): The reaction that dictates if the role is added or not
        """

        # flags
        reaction_is_unicode: bool = False

        # Check if the message_id given is an Integer
        if not message_id.isdigit():

            # NOTE: Following code can be extracted into Utils.send()
            # function, where it responds to the interaction and
            # deletes after a few seconds
            await interaction.response.send_message("`message_id` is not an integer!")
            await asyncio.sleep(5)
            msg = await interaction.original_response()
            await msg.delete()
            return

        # Check if the reaction is built in unicode
        for char in reaction:
            if ord(char) > 127:
                reaction_is_unicode = True
                break

        # Find the correct emoji
        # if it isn't unicode reaction
        emoji: discord.Emoji = None
        if not reaction_is_unicode:
            match = re.search(r":(\d+)", reaction)
            if match:
                emoji = await interaction.guild.fetch_emoji(int(match.group(1)))
            else:
                interaction.response.send_message("Not a valid emoji!")
                await asyncio.sleep(5)
                msg = await interaction.original_response()
                await msg.delete()
                return

        try:

            data = Utils.read_from_json("res/json/reaction_roles.json")

            # If the guild doesnt exist in json
            # add it
            if str(interaction.guild_id) not in data:
                data[str(interaction.guild_id)] = {}

                # If the message doesn't exist
                # create a new entry for it
                if message_id not in data[str(interaction.guild_id)]:
                    data[str(interaction.guild_id)][message_id] = {}
                    data[str(interaction.guild_id)][message_id][
                        emoji.id if emoji is not None else reaction
                    ] = role.id
                else:
                    data[str(interaction.guild_id)][message_id][
                        emoji.id if emoji is not None else reaction
                    ] = role.id

            else:
                # The guild already exits,
                # add message entry if it doesn't
                if message_id not in data[str(interaction.guild_id)]:
                    data[str(interaction.guild_id)][message_id] = {}
                    data[str(interaction.guild_id)][message_id][
                        emoji.id if emoji is not None else reaction
                    ] = role.id
                else:
                    data[str(interaction.guild_id)][message_id][
                        emoji.id if emoji is not None else reaction
                    ] = role.id

            with open("res/json/reaction_roles.json", "w") as reaction_file:
                json.dump(obj=data, fp=reaction_file, indent=4, ensure_ascii=False)
            reaction_file.close()

            # Get Channel so the message can be found
            # and given the reaction
            channel = interaction.channel

            await channel.get_partial_message(message_id).add_reaction(
                emoji if emoji is not None else reaction
            )

        except Exception as exc:
            await interaction.response.send_message(exc)
            return

        message = interaction.guild.get_channel(int(message_id))

        #
        jump_url = (
            f"[message.]({message.jump_url})"
            if message
            else f"[message.](https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}/{message_id})"
        )

        # Log to Lj
        self.bot.lj.log(
            "emperor.cogs.mod.reactionroles.create",
            f"ReactionRole setup for {message_id}",
        )

        await interaction.response.send_message(
            f"Successfully added reaction role to {jump_url}",
            ephemeral=True,
        )

    @reaction_group.command(
        name="remove",
        description="Removes the link between reaction and role in a message",
    )
    async def reaction_remove(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message_id: str,
        reaction: str,
    ):
        """
        Remove the link between reaction and role in a message.

        Args:
            channel (discord.TextChannel): The channel the message is in.
            message_id (str): The message id of where the link is in.
            reaction (str): The reaction the forms the link.
        """
        reaction_is_unicode: bool = False

        # Check the message id
        if not message_id.isdigit():
            await interaction.response.send_message("`message_id` is not an integer!")
            await asyncio.sleep(2)
            msg = await interaction.original_response()
            await msg.delete()
            return

        message = await channel.fetch_message(int(message_id))

        # Making sure the message exits
        if message is None:
            await interaction.response.send_message(
                "Incorrect message id given, no message could be found in the guild"
            )
            await asyncio.sleep(2)
            msg = await interaction.original_response()
            await msg.delete()
            return

        # Check if the reaction is built in unicode
        for char in reaction:
            if ord(char) > 127:
                reaction_is_unicode = True
                break

        # Find the correct emoji
        # if it isn't unicode reaction
        emoji: discord.Emoji = None
        if not reaction_is_unicode:
            match = re.search(r":(\d+)", reaction)
            if match:
                emoji = await interaction.guild.fetch_emoji(int(match.group(1)))
            else:
                interaction.response.send_message("Not a valid emoji!")
                await asyncio.sleep(5)
                msg = await interaction.original_response()
                await msg.delete()
                return

        try:
            data = Utils.read_from_json("res/json/reaction_roles.json")

            # Make sure the Guild/Message/Reaction
            # is in the file before deleting it
            if data[str(interaction.guild_id)]:
                if data[str(interaction.guild_id)][message_id]:
                    if data[str(interaction.guild_id)][message_id][
                        emoji.id if emoji is not None else reaction
                    ]:
                        del data[str(interaction.guild_id)][message_id][
                            emoji.id if emoji is not None else reaction
                        ]

            # The changes must be saved
            with open("res/json/reaction_roles.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
            json_file.close()

            # Remove the reaction in the message
            await message.clear_reaction(emoji.id if emoji is not None else reaction)

            # Inform the user that it has been done
            await interaction.response.send_message(
                "The link between reaction and role has been deleted on the message",
                ephemeral=True,
            )

        except Exception as exc:
            # Inform the user that something has gone wrong
            # NOTE: Better handling of catch statements i.e. NotFound can be separate
            # catch, and KeyError could be another.
            await interaction.response.send_message(
                f"Exception was raised!\n{exc}", ephemeral=True
            )

    # Create commands #
    @create_group.command(
        name="embed",
        description="Create an embed using json code or through parameters",
    )
    async def create_embed(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel],
        embed_json: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[discord.Member] = None,
    ):
        """
        Create an embed from json code given by the user or through parameters

        Args:
            channel (Optional[discord.TextChannel]): The channel to post the embed in. Defaults to where the command was run.
            embed_json (Optional[str]): Embed JSON code.
            title (Optional[str], optional): The title of the embed. Defaults to None.
            description (Optional[str], optional): Description of the embed. Defaults to None.
            author (Optional[discord.Member], optional): Author of the embed. Defaults to None.

        Returns:
            An embed on successfull run

        """

        # If json is given, then make the
        # embed from json instead of anything else
        if embed_json is not None:
            try:
                # Checking if the json data is correct
                # syntax wise
                data = json.loads(embed_json)

                # Send the embed from json code
                # and break away from the function
                await interaction.response.send_message(
                    embed=discord.Embed.from_dict(data)
                )
                return

            except Exception as exc:
                if hasattr(exc, "message"):
                    await interaction.response.send_message(
                        f"JSONDecoder error: {exc.message}"
                    )
                else:
                    await interaction.response.send_message(f"JSONDecoder error: {exc}")
        else:

            custom_embed = discord.Embed()

            if title is not None:
                custom_embed.title = title

            # Add description if not None
            if description is not None:
                custom_embed.description = description.replace(r"\n", "\n")

            # Add colour, footor & author to the embed
            # only if the embed has any data
            if bool(custom_embed):
                custom_embed.color = self.bot.config.COLOUR
                custom_embed.set_footer(
                    text=f"{self.bot.user.name} | by UOW School of Computing Dev team",
                    icon_url=self.bot.user.display_avatar.url,
                )

                # Add author if not None
                if author is not None:
                    custom_embed.set_author(
                        name=author.name, icon_url=author.display_avatar.url
                    )

            else:
                await interaction.response.send_message(
                    "`CREATE ERROR`: All parameters were left empty!", ephemeral=True
                )
                return

            # Checking to see which channel
            # the embed should be sent in
            if channel is not None:
                embed_message = await channel.send(embed=custom_embed)
            else:
                embed_message = await interaction.channel.send(embed=custom_embed)

            await interaction.response.send_message(
                f'Successfully created [{"" if title is None else f"{title}"}]({embed_message.jump_url}) embed.',
                ephemeral=True,
            )


async def setup(bot):
    """
    Setup function for the cog

    Args:
        bot (discord.ext.commands.Bot): Instance of the bot class
    """

    # Make an discord.Object for each
    # guild in the list
    guild_objects: list(discord.Object) = []
    for guild in bot.config.GUILD_ID:
        guild_objects.append(discord.Object(id=guild))

    await bot.add_cog(Mod(bot), guilds=(guild_objects))
