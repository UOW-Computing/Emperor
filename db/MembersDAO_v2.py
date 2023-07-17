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
from db.Member_v2 import Member
from db.AbstractDAO import AbstractDAO


class MembersDAO(AbstractDAO):

    def __init__(self, connection_pool):
        # Set up the parent class, AbstractDAO
        super(MembersDAO, self).__init__(connection_pool)

        # Configure all the tables
        # Each tuple holds
        # the name of the table
        # and the column names in order
        self.__members_table: tuple[str, str] = (
            "members_table",
            "(discord_id, extras, guilds)"
        )

        self.__xp_table: tuple[str, str] = (
            "xp_table",
            "(discord_id, xp_level, xp_points)"
        )

        self.__repu_table: tuple[str, str] = (
            "repu_table",
            "(discord_id, reputation, last_repu_from, last_repu_to)"
        )

    ##################################### 
    #         Core API Calls            #
    #####################################

    async def get_member(self, discord_id: int) -> Member:
        rec_mem = await super()._read_record(self.__members_table[0], discord_id)
        rec_xp = await super()._read_record(self.__xp_table[0], discord_id)
        rec_repu = await super()._read_record(self.__repu_table[0], discord_id)

        return Member.create_member_from_records(rec_mem, rec_xp, rec_repu)
    
    async def get_member_extras(self, discord_id: int) -> tuple[int, dict]:
        result = await super()._read_record(self.__members_table[0], discord_id)

        return tuple([discord_id, result['extras']])

    # noinspection PyMethodMayBeStatic
    async def get_members_guilds(self, discord_id: int) -> str:
        return "This method has not been fully implemented, thus will not change as of yet."

    #####################################
    #           XP API Calls            #
    #####################################

    # Getters
    async def get_member_xp(self, discord_id) -> tuple[int, int, int]:
        result = await super()._read_record(self.__xp_table[0], discord_id)

        return tuple(result)

    async def get_member_xp_level(self, discord_id) -> tuple[int, int]:
        result = await self.get_member_xp(discord_id)

        return tuple([result[0], result[1]])

    async def get_member_xp_points(self, discord_id) -> tuple[int, int]:
        result = await self.get_member_xp(discord_id)

        return tuple([result[0], result[2]])

    #####################################
    #       REPUTATION API Calls        #
    #####################################

    # Getters
    async def get_member_reputation_record(self, discord_id) -> tuple[int, int, int, int]:
        result = await super()._read_record(self.__repu_table[0], discord_id)

        return tuple(result)

    async def get_member_reputation(self, discord_id) -> tuple[int, int]:
        result = await self.get_member_reputation_record(discord_id)

        return tuple([result[0], result[1]])

    async def get_member_last_reputation_from(self, discord_id) -> tuple[int, int]:
        result = await self.get_member_reputation_record(discord_id)

        return tuple([result[0], result[2]])

    async def get_member_last_reputation_to(self, discord_id) -> tuple[int, int]:
        result = await self.get_member_reputation_record(discord_id)

        return tuple([result[0], result[3]])

    async def commit(self, member: Member):
        """
        Updates the database Record with information from the Member object. \n
        Any changes made to the Member class has to be committed through this function.
        """
        await super()._update_record(self.__members_table[0],
                                     member.get_discord_id,
                                     {"extras": member.get_extras})

        await super()._update_record(self.__xp_table[0],
                                     member.get_discord_id,
                                     {"xp_level": member.get_xp_level,
                                      "xp_points": member.get_xp_points})

        await super()._update_record(self.__repu_table[0],
                                     member.get_discord_id,
                                     {"reputation": member.get_reputation,
                                      "last_repu_from": member.get_last_reputation_from,
                                      "last_repu_to": member.get_last_reputation_to})
