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
from dataclasses import dataclass
from typing import Any

from asyncpg import Record


# Member Datatype
@dataclass
class Member:
    # Core Attributes
    __DISCORD_ID: int
    __extras: dict

    # XP related Attribute
    # will hold a tuple first value is
    # the level, second is the points
    __xp: tuple[int, int]

    # Reputation related Attribute
    __repu: int
    # Dictionary holding the values
    # using the key 'to' or 'from'
    # it will return the id of the user
    __last_repu: dict

    def __init__(self, discord_id: int,
                 extras: dict | None = None,
                 xp: tuple[int, int] = (0, 0),
                 reputation: int = 0,
                 last_reputations: dict | None = None):

        self.__DISCORD_ID = discord_id
        self.__xp = xp
        self.__repu = reputation

        if last_reputations is None:
            self.__last_repu = {"to": None, "from": None}
        else:
            self.__last_repu = last_reputations
        if extras is None:
            self.__extras = {}
        else:
            self.__extras = extras

    @classmethod
    def create_member(cls, discord_id: int):
        """
        Initialize all values to default
        """
        return cls(discord_id)

    @classmethod
    def create_member_from_records(cls, rec_mem: Record, rec_xp: Record, rec_repu: Record):
        """
        Initialize all values based on the records given, used for existing data values

        :param Record rec_mem: record from the members table
        :param Record rec_xp: record from the experience point table
        :param Record rec_repu: record from the reputation table

        :return: An instance of Member based on the input values
        """
        return cls(discord_id=rec_mem['discord_id'],
                   extras=rec_mem['extras'],
                   xp=(rec_xp['xp_level'], rec_xp['xp_points']),
                   reputation=rec_repu['reputation'],
                   last_reputations={"to": rec_repu['last_repu_to'], "from": rec_repu['last_repu_from']})

    @classmethod
    def create_member_from_record(cls, record: Record):
        """
        Initialize all values based on the Member Record given in.

        :param Record record: Record taken from the members table

        :return: An instance of Member, with default values
        """
        return cls(
            discord_id=record['discord_id'],
            extras=record['extras'])

    ##################################################
    #                                                #
    #                Core Functions                  #
    #                                                #
    ##################################################

    # Getters

    @property
    def get_discord_id(self) -> int:
        return self.__DISCORD_ID

    @property
    def get_extras(self) -> dict:
        return self.__extras

    def get_extra(self, key: str) -> Any | None:
        try:
            return self.__extras[key]
        except KeyError:
            print(f"extras does not contain value for '{key}'")
            return None

    # Setters

    def set_extras(self, extras_dict: dict):
        """
        Set the extras dictionary to the given dictionary.

        :param extras_dict: the new dictionary
        """
        self.__extras = extras_dict

    def add_extras_key_value(self, key: Any, value: Any) -> bool:
        try:
            self.__extras[key] = value
            return True
        except TypeError:
            print("Bad key given in, please check you are not giving in a mutable key.")
            return False

    ##################################################
    #                                                #
    #                XP Functions                    #
    #                                                #
    ##################################################

    # Getters
    @property
    def get_xp(self) -> tuple[int, int]:
        return self.__xp

    @property
    def get_xp_level(self) -> int:
        return self.__xp[0]

    @property
    def get_xp_points(self) -> int:
        return self.__xp[1]

    # Setter
    def set_xp(self, levels: int = 0, points: int = 0) -> None:
        """
        Increase the xp level or points.

        NOTE: You can decrease level/points by giving in negative values.

        Example::

            # Increase levels by 5
            set_xp(levels=5)
            # Decrease levels by 2, but increase points by 3
            set_xp(levels=-2, points=3)
            # Decrease points by 100
            set_xp(points=-100)

        :param int levels: amount to increase/decrease levels by
        :param int points: amount to increase/decrease points by

        """
        self.__xp = (self.__xp[0] + levels, self.__xp[1] + points)

    ##################################################
    #                                                #
    #             REPUTATION Functions               #
    #                                                #
    ##################################################

    # Getters

    @property
    def get_reputation(self) -> int:
        return self.__repu

    @property
    def get_last_reputation_from(self) -> int | None:
        return self.__last_repu['from']

    @property
    def get_last_reputation_to(self) -> int | None:
        return self.__last_repu['to']

    # Setters

    def set_reputation(self, rep: int):
        """
        Set the reputation of the user.
        Increase/decrease the reputation based on the rep given.
        Negative values will decrease the reputation.

        Example::

            # Increase reputation by 5
            set_reputation(5)
            # Decrease reputation by -5
            set_reputation(-5)

        :param int rep: amount to increase/decrease reputation by
        """

        self.__repu += rep

    def set_reputation_last_from(self, rep_from: int):
        """
        Stores the person's discord id who gave the last reputation
        to the user.

        :param int rep_from: the discord_id of the user who gave reputation
        """
        self.__last_repu['from'] = rep_from

    def set_reputation_last_to(self, rep_to: int):
        """
        Stores the person's discord id who was given reputation by the user

        :param int rep_to: the discord_id of the user who gave reputation
        """
        self.__last_repu['to'] = rep_to
