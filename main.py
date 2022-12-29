import os
import discord

from dotenv import load_dotenv
from src.Emperor import Emperor
from src.config import Settings

bot = discord.Bot()


load_dotenv()

config = Settings()

print(
    f"""
 _____
|   __|_____ ___ ___ ___ ___ ___
|   __|     | . | -_|  _| . |  _|
|_____|_|_|_|  _|___|_| |___|_|
            |_| © 2022 nukestye

Welcome to Emperor v{os.getenv('BOT_ENV_VERSION')}!
Loading cogs...\n
"""
)

emperor = Emperor(config)

emperor.run(config.TOKEN)
