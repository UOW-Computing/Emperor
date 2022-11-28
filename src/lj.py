import time
import discord
from src.util import logChannelID


class LJ:

    bot = None
    logfile = None

    def __init__(self, bot) -> None:
        if logChannelID is None:
            self.WARN("logger/init", "Channel ID is undefined!")
        self.logfile = f'logs-{time.ctime(time.time())}'

        self.bot = bot

    @staticmethod
    def WARN(context: str = "main", message: str = "Unknown error occured! Ensure all procedures are working correctly") -> None:
        # Print ot console
        format = f'[{time.ctime(time.time())}] [{context}] \x1b[2;30;41m[WARNING] {message}\x1b[0m'
        print(format)

        # Save to file
        with open('logs', 'a') as logFile:
            logFile.write(format + "\n")
        logFile.close()

    @staticmethod
    def LOG(context: str = "main", message: str = "No context provided") -> None:
        # print to console
        format = f'[{time.ctime(time.time())}] [{context}]: {message}'
        print(format)

        # save to file
        with open('logs', 'a') as logFile:
            logFile.write(format + "\n")
        logFile.close()

    async def LOGChannel(self, message: discord.Message) -> None:
        if logChannelID is None:
            self.WARN("logger/LogChannel",
                      "Channel ID is undefined, and an attempt was made to log in text channels.")
        logChannel = await message.guild.fetch_channel(logChannelID)

        # form a embed
        embed = discord.Embed(title="Content",
                              description=f'{message.content}',
                              timestamp=message.created_at,
                              color=discord.Color.from_rgb(128, 0, 128))
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.display_avatar)
        embed.set_thumbnail(url=message.author.display_avatar)
        embed.add_field(
            name="Send by", value=f'<@{message.author.id}>', inline=True)
        embed.add_field(
            name="IDs", value=f'```\nMessage:\t{message.id}\nUser:\t{message.author.id}```', inline=True)
        embed.add_field(
            name="Channel", value=f'<#{message.channel.id}>\nChannel ID: `{message.channel.id}`')

        await logChannel.send(embed=embed)

    def ljERROR():
        pass
