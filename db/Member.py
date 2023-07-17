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

# version: 1
# author: Breno & nukestye

from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Member:
    """
    This dataclass serves as a cheap way of storing a record instead of querying the database all the time. \n
    The member.get_all @property will return all the info about that record.
    For now, it's mostly being used for testing because it does not update the database if you modify its values.
    """
    discord_id: int
    university_id: int
    xp_level: int
    elo_rating: int
    bot_level: int
    about_me: int

    class Enum(StrEnum):
        DISCORD_ID: str = "discord_id"
        UNIVERSITY_ID: str = "university_id"
        XP_LEVEL: str = "xp_level"
        ELO_RATING: str = "elo_rating"
        BOT_LEVEL: str = "bot_level"
        ABOUT_ME: str = "about_me"

    @property
    async def info(self):
        """
        Returns all the information about this Record/Member.\n
        Mostly used for console printing(dev).\n
        If you need to use the individual property:
        ex: Member.about_me
        """
        return f"Discord ID: {self.discord_id}\nUniversity ID: {self.university_id}\nXP Level: {self.xp_level}\nELO " \
               f"Rating: {self.elo_rating}\nBot Level: {self.bot_level}\nAbout Me: {self.about_me}"

    @property
    async def info_tuple(self) -> tuple:
        """
        Returns all the information about this Record/Member in tuple form.\n
        If you need to use the individual property:
        ex: Member.about_me
        """
        return self.discord_id, self.university_id, self.xp_level, self.elo_rating, self.bot_level, self.about_me

    async def set_field(self):
        pass
