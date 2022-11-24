from discord.ext import commands
import discord
from src.lj import LJ

# Nzk3OTE1OTUxNDU3NzYzMzI4.GMKpcK.YKxB0lQb4CYB-Zm3_tYhf4AHhSbXM1KXx_oDRA
# ----------------------------------
PREFIX = "/"

logChannelID = '1043986118258987008'
# ----------------------------------


class Emperor(commands.Bot):

    log = LJ()

    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=PREFIX, description="Help me", intents=intents)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name="<!>"))

        print(f'BOT READY: {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        self.log.LOG(context=f'{message.guild.name}/{message.channel.name}',
                     message=f'{message.author} [ID: {message.id}] {message.content}')
        await self.process_commands(message)

    async def on_command(self, ctx):
        self.log.LOG("main/CommandHandler", f"Executing {ctx.command}")
