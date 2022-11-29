import time
import discord
from src.util import LOGCHANNELID


class LJ:

    bot = None
    logfile = None

    def __init__(self, bot) -> None:
        if LOGCHANNELID is None:
            self.WARN("logger/init", "Channel ID is undefined!")
        self.logfile = f'logs-{time.ctime(time.time())}'

        self.bot = bot

    @staticmethod
    def WARN(context: str = "main",
             msg: str = "Unknown error occured!") -> None:

        # get the current time
        ctime = time.ctime(time.time())
        # Print ot console
        WARNformat = f'[{ctime}] [{context}] \x1b[2;30;41m[WARN] {msg}\x1b[0m'
        print(WARNformat)

        # Save to file
        with open('logs', 'a', encoding='utf-8') as logFile:
            logFile.write(WARNformat + "\n")
        logFile.close()

    @staticmethod
    def LOG(context: str = "main",
            message: str = "No context provided") -> None:
        # print to console
        LOGformat = f'[{time.ctime(time.time())}] [{context}]: {message}'
        print(LOGformat)

        # save to file
        with open('logs', 'a', encoding='utf-8') as logFile:
            logFile.write(LOGformat + "\n")
        logFile.close()

    async def LOGChannel(self, message: discord.Message) -> None:
        if LOGCHANNELID is None:
            self.WARN("logger/LogChannel",
                      "Log Channel ID is undefined, cannot log inside servers")
        try:
            logChannel = await message.guild.fetch_channel(LOGCHANNELID[0])
        except:
            logChannel = await message.guild.fetch_channel(LOGCHANNELID[1])


        # form a embed
        e = discord.Embed(title="Content",
                              description=f'{message.content}',
                              timestamp=message.created_at,
                              color=discord.Color.from_rgb(128, 0, 128))
        e.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.display_avatar)
        e.set_thumbnail(url=message.author.display_avatar)
        e.add_field(
            name="Send by", value=f'<@{message.author.id}>', inline=True)
        e.add_field(name="IDs",
                    value=f'```\nMessage:\t{message.id}\nUser:\t{message.author.id}```',
                    inline=True)
        e.add_field(name="Channel",
                    value=f'<#{message.channel.id}>\nID: `{message.channel.id}`')

        await logChannel.send(embed=e)

    # def ljERROR():
    #     pass
