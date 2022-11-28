from discord.ext import commands
from src.lj import LJ
from src.util import *

import discord


class Emperor(commands.Bot):

    log = None

    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True

        self.log = LJ(self)

        super().__init__(command_prefix=PREFIX, description="Help me", intents=intents)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name="<!>"))

        print(f'BOT READY: {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return None

        # Figure out if the message is from DM or guild
        await self.log.LOGChannel(message=message)
        self.log.LOG(context=f'{message.guild.name}/{message.channel.name}',
                     message=f'{message.author} [MSG ID: {message.id}] {message.content}')
        await self.process_commands(message)

    async def on_command(self, ctx):
        self.log.LOG("main/CommandHandler", f"Executing {ctx.command}")
