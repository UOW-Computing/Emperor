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
        Discord_ID: str = "discord_id"
        University_ID: str = "university_id"
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
