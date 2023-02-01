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


import discord

from datetime import datetime
from discord.ext import commands
from src.config import Settings
from src.Lj import Lj


class Emperor(commands.Bot):

    # pylint: disable=invalid-name
    config: Settings = None
    lj: Lj = None
    uptime: datetime = None
    # pylint: enable=invalid-name

    def __init__(self, p_intents: discord.Intents, p_config: Settings) -> None:

        self.config = p_config
        self.lj = Lj()

        super().__init__(
            description="Discord made by School of Computing Dev team.",
            command_prefix=commands.when_mentioned_or(self.config.BOT_PREFIX),
            intents=p_intents,
        )

    async def setup_hook(self):
        """
        Loads all the cogs into the bot
        """
        for cog in self.config.COGS:
            try:
                await self.load_extension("cogs." + cog)
            except Exception as exc:
                print(
                    f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
                )

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="e!")
        )
        self.lj.log("emperor.onready", f"Logged on as {self.user} (ID: {self.user.id})")

        self.uptime = datetime.now()

    async def on_message(self, msg: discord.Message):

        if msg.author.bot:
            return

        def check_for_message():
            """
            Insures that if an attachment is given the content is not left blank

            Args:
                msg (discord.Message): The message to parser through

            Returns:
                str: Message content if it had text
                url: Url(s) if the message had no content
            """
            if len(msg.attachments) != 0:
                attachments_url = " ".join(
                    attachment.url for attachment in msg.attachments
                )

                return f"{msg.content} \t {attachments_url}"

            return msg.content

        self.lj.log(
            f"emperor.message    {msg.guild.name}.{msg.channel.name}",
            f"{msg.author}: {check_for_message()}",
        )
        await self.process_commands(msg)
