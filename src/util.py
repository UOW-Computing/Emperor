import discord

PREFIX = "/"
GUILD_ID = [573602053352456193]
logChannelID = '1043986118258987008'

# Depreciated method


def strip_message(message: discord.Message) -> list:
    b = message.content.strip(PREFIX)
    cmd_content = b.split(" ")
    # clean message from "" or " "
    cmd_content = __clean(cmd_content)
    return cmd_content

# Depreciated method


def __clean(message: list) -> list:
    return list(filter(("").__ne__, message))


def no_args_erro(member, msg: str) -> discord.Embed:
    embed = discord.Embed(title='Arugments needed',
                          description=f'`{msg}` needs arguments', color=0x98FB98)
    embed.set_author(name="Emperor", url='')

    return embed
