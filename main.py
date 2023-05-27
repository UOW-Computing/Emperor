"""
Emperor, discord bot for school of computing
Copyright (C) 2022-2023  School of Computing Dev Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord

from discord.ext import commands
from dotenv import load_dotenv
from src.ServerUtils import Utils
from src.config import Settings
from src.Emperor import Emperor

load_dotenv()

config = Settings()

Utils.print_branding()  # Prints Emperor Logo Branding

# Sending the intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.reactions = True

Emperor = Emperor(intents, config)

Emperor.run(config.TOKEN)
