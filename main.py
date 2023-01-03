import os
import typing
import discord


from dotenv import load_dotenv
from src.config import Settings
from src.Emperor import Emperor
from discord.ext import commands

load_dotenv()

config = Settings()

print(
    f"""
 _____
|   __|_____ ___ ___ ___ ___ ___
|   __|     | . | -_|  _| . |  _|
|_____|_|_|_|  _|___|_| |___|_|
            |_| © 2022 nukestye

Welcome to Emperor v{os.getenv('BOT_ENV_VERSION')}!\n
"""
)

# Sending the intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

emperor = Emperor(intents, config)


# Command used to sync command changes
@emperor.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: commands.Context, guilds: commands.Greedy[discord.Object],
  spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

emperor.run(config.TOKEN)
