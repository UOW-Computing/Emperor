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

# pylint: disable=too-few-public-methods
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Secret information gathered from a file

    """

    # Hardcoded values in env
    COGS: list
    COLOUR: int

    # Changeable fields
    TOKEN: str
    BOT_PREFIX: str
    OPENAI_KEY: str
    GITHUB_KEY: str
    GUILD_ID: int | list
    LOG_CHANNEL_IDs: str | dict
    STAFF_IDS: dict

    class Config:
        """
        Config class that knows where the information is stored
        """

        env_file = ".env"
        env_file_encoding = "utf-8"
