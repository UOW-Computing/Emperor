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

        # Create the tables
        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                """
                create table if not exists members_table (
                    discord_id bigint not null primary key,
                    extras json,
                    guilds bigint[]
                );


                create table if not exists xp_table(
                    discord_id bigint primary key not null,
                    xp_lvl int not null default 0,
                    xp_points int not null default 0,

                    CONSTRAINT discord_id
                        foreign key (discord_id)
                        references members_table(discord_id)
                        on delete cascade
                );


                create table if not exists repu_table(
                    discord_id bigint primary key not null,
                    reputation int not null default 0,
                    last_repu_from int default -1,
                    last_repu_to int default -1,

                    CONSTRAINT discord_id
                        foreign key (discord_id)
                        references members_table(discord_id)
                        on delete cascade
                    );
                """
            )

        self.m = MembersDAO(self.__connection_pool)
        self.g = GuildsDAO(self.__connection_pool)
