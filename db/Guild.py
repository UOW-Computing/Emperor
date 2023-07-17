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
import datetime

from dataclasses import dataclass
from enum import StrEnum

from asyncpg import Record


@dataclass
class Guild:
    #########################################
    guild_id: int
    description: str | None
    created_at: datetime.date
    joined_at: datetime.date
    members_count: int
    owner_id: int

    ########################################

    class Enum(StrEnum):
        GUILD_ID: str = "guild_id"
        DESCRIPTION: str = "description"
        CREATED_AT: str = "created_at"
        JOINED_AT: str = "joined_at"
        MEMBERS_COUNT: str = "members_count"
        OWNER_ID: str = "owner_id"

    def __init__(self, record: Record):
        self.guild_id = record['guild_id']
        self.description = record['description']
        self.created_at = record['created_at']
        self.joined_at = record['joined_at']
        self.members_count = record['members_count']
        self.owner_id = record['owner_id']

    def __int__(self,
                guild_id: int,
                description: str,
                created_at: datetime.date,
                joined_at: datetime.date,
                members_count: int,
                owner_id: int):
        self.guild_id = guild_id
        self.description = description
        self.created_at = created_at
        self.joined_at = joined_at
        self.members_count = members_count
        self.owner_id = owner_id
