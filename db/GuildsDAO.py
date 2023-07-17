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

from datetime import date, datetime

from db.AbstractDAO import AbstractDAO
from db.Guild import Guild


class GuildsDAO(AbstractDAO):
    def __init__(self, connection_pool):
        super(GuildsDAO, self).__init__(connection_pool)
        self.main_table = (
            "guilds",
            "(guild_id, description, created_at, joined_at, members_count, owner_id)"
        )
        self.__config_table = (
            "guildConfigs",
            "(guild_id, bot_prefix, staff_ids, log_channel_id)"
        )
        self.__connection_pool = connection_pool

    async def set_up(self):

        # NOTE(nuke): this needs to be moved out of the DAOs and into a preliminary file
        # that gets run at start of runtime, ie 'on_ready' in Emperor.py
        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS guilds (
                    guild_id 	bigint NOT NULL,
                    description	text,
                    created_at	DATE NOT NULL,
                    joined_at   DATE NOT NULL,
                    members_count int NOT NULL,
                    owner_id    int NOT NULL
                )
                """
            )

    ####################################
    #                                  #
    #          Guild Functions         #
    #                                  #
    ####################################

    async def get_guild_record(self, guild_id: int) -> Guild | None:

        if not isinstance(guild_id, int):
            print("'guild_id' must be int, not any other type.")

        query_result = await super()._read_record(self.main_table[0], guild_id)

        if len(query_result) != 0:
            return Guild(query_result)

        print("Guild does not exist")
        return None

    async def check_if_guild_exists(self, guild_id: int) -> bool:
        if not isinstance(guild_id, int):
            print("'guild_id' must be int, not any other type.")

        query_result = await super()._read_record(self.main_table[0], guild_id)

        if len(query_result) != 0:
            return True

        return False

    @property
    async def get_all_guild_records(self):
        results = await super()._get_all_records(self.main_table[0])

        l: list = []

        for i in range(0, len(results)):
            l.append(Guild(results[i]))

        return l

    async def create_test(self, v: int):
        return await super()._create_record(self.main_table[0], {
            "guild_id": v,
            "description": 'none',
            "created_at": str(datetime.now().date()),
            "joined_at": str(datetime.now().date()),
            "members_count": 5,
            "owner_id": 1
        })

    async def create_guild_record(self,
                                  guild: discord.Guild,
                                  joined_at: date) -> bool:

        # All Information used in the function is form
        # discord.Guild only therefore is needed
        if not isinstance(guild, discord.Guild):
            print("Please pass in an 'discord.Guild' object!")
            return False

        # Prevents sql from throwing errors
        # if the value is not date type
        if not isinstance(joined_at, date):
            print("Please pass in a date for 'joined_at'!")
            return False

        # Use the abstract ._create_record function
        # to create a record of the guild
        # Debug: True if recorded has been created
        return await super()._create_record(self.main_table[0], {
            "guild_id": guild.id,
            "description": guild.description if guild.description is not None else "none",
            "created_at": guild.created_at.strftime('%Y-%m-%d'),
            "joined_at": joined_at.strftime('%Y-%m-%d'),
            "members_count": guild.member_count,
            "owner_id": guild.owner_id
        })

    ####################################
    #                                  #
    #      Guild Config Functions      #
    #                                  #
    ####################################

    async def new_server_config(self,
                                guild_id: int,
                                bot_prefix: str = "e!",
                                staff_roles: list[int] = list[-1],
                                log_channel_id: int = 0
                                ):
        await self._create_record(self.__config_table[0], {
            "guild_id": guild_id,
            "bot_prefix": bot_prefix,
            "staff_ids": staff_roles,
            "log_channel_id": log_channel_id
        })
