import os
import discord

from dotenv import load_dotenv
from src.Emperor import Emperor

# TODO: 
# - Make log channel a dict inside .env file
# - Add setup.py into VC
# - More General Commands
# - Add changelog.md into VC 


bot = discord.Bot()
__cogs__ = ['admins', 'generals']

load_dotenv()


emperor = Emperor()

print(f"""
                                                          
 _____                           
|   __|_____ ___ ___ ___ ___ ___ 
|   __|     | . | -_|  _| . |  _|
|_____|_|_|_|  _|___|_| |___|_|  
            |_| © 2022 nukestye                 

Welcome to Emperor v{os.getenv('BOT_ENV_VERSION')}!
Loading cogs...\n
""")

for cog in __cogs__:
	print(f'Loaded {cog}')
	emperor.load_extension(f'cogs.{cog}')

emperor.run(os.getenv('TOKEN'))

# print(eval(os.getenv('LOG_CHANNEL_ID'))['573602053352456193'])
