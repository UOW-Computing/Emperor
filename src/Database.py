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

import asyncpg

from discord.ext import commands
from typing import Dict

from db.GuildsDAO import GuildsDAO
from db.MembersDAO import MembersDAO


class Database:
    """

    """
    bot: commands.Bot

    m: MembersDAO
    g: GuildsDAO

    def __init__(self, bot: commands.Bot):
        # set the reference for
        # the bot
        self.__connection_pool = None
        self.bot = bot

    async def create_database(self, credentials: Dict[str, str]):
        self.__connection_pool = await asyncpg.create_pool(
            database=credentials['database'],
            user=credentials['username'],
            password=credentials['password']
        )

        self.m = MembersDAO(self.__connection_pool)
        self.g = GuildsDAO(self.__connection_pool)
