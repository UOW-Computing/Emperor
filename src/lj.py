import os 
import time
import discord


class Lj:

    bot = None
    log_file = None

    def __init__(self, bot) -> None:
        if int(eval(os.getenv('LOG_CHANNEL_ID'))) is None:
            self.warn("logger/init", "Channel ID is undefined!")
        self.log_file = f'logs-{time.ctime(time.time())}'

        self.bot = bot

    @staticmethod
    def warn(context: str = "main",
             msg: str = "Unknown error occured!") -> None:

        # get the current time
        ctime = time.ctime(time.time())
        # Print ot console
        warn_format = f'[{ctime}] [{context}] \x1b[2;30;41m[WARN] {msg}\x1b[0m'
        print(warn_format)

        # Save to file
        with open('logs', 'a', encoding='utf-8') as logFile:
            logFile.write(warn_format + "\n")
        logFile.close()

    @staticmethod
    def log(context: str = "main",
            message: str = "No context provided") -> None:
        # print to console
        log_format = f'[{time.ctime(time.time())}] [{context}]: {message}'
        print(log_format)

        # save to file
        with open('logs', 'a', encoding='utf-8') as logFile:
            logFile.write(log_format + "\n")
        logFile.close()
