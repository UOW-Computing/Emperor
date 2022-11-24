import discord
import os
from dotenv import load_dotenv
from src.Emperor import Emperor


bot = discord.Bot()
__cogs__ = ['cogs.admins']

load_dotenv()


emperor = Emperor()


for cog in __cogs__:
    emperor.load_extension(cog)

emperor.run(os.getenv('TOKEN'))
