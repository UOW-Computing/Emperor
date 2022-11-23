PREFIX = "/"
import discord

from enum import Enum


def strip_message(message: discord.Message) -> list:
	b = message.content.strip(PREFIX)
	cmd_content = b.split(" ")
	# clean message from "" or " "
	cmd_content = __clean(cmd_content)
	return cmd_content


def __clean(message: list) -> list:
	return list(filter(("").__ne__, message))



def no_args_erro(member, msg: str) -> discord.Embed:
	embed = discord.Embed(title='Arugments needed', description=f'`{msg}` needs arguments', color=0x98FB98)
	embed.set_author(name="Emperor", url='')

	return embed



class TerminalColours(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
