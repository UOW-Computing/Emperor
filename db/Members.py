from dataclasses import dataclass


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

    @property
    async def info(self):
        """Returns all the information about this Record/Member.\n
        Mostly used for console printing(dev).\n
        If you need to use the individual property:
        ex: Member.about_me """
        return f"Discord ID: {self.discord_id}\nUniversity ID: {self.university_id}\nXP Level: {self.xp_level}\nELO Rating: {self.elo_rating}\nBot Level: {self.bot_level}\nAbout Me: {self.about_me}"

    async def set_field(self):
        return