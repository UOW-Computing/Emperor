import discord

from db.Member import Member
from db.AbstractDAO import AbstractDAO


class MembersDAO(AbstractDAO):
    """
    MembersDAO class is responsible for acting as the API between Emperor and its Database.\n
    Any changes to the users of the database should be done through MembersDAO not AbstractDAO.\n
            Functions
        - create_member()       - Creates a record
        - delete_member()       - Deletes a record
        - update_record()       - Master update all field in a record
        - get_record()          - Returns a Record as a Member Dataclass
        - update_field()        - Change a specific field
        - commit()              - Pushes changes from a Member class to the Database\n
        Properties(Getters)
            - get_all_records   - Returns all records within the table
            - get_field         - Returns a specific field from the parsed column
     """

    def __init__(self, connection_pool):
        """
        :param connection_pool: Inherited connection pool from AbstractDAO
        """
        super(MembersDAO, self).__init__(connection_pool)

        self.__table = ("members", "(discord_id, university_id, xp_level, elo_rating, bot_level)")
        self.__connection_pool = connection_pool

    async def create_member_record(self, member: discord.Member):
        if not isinstance(member, discord.Member):
            print("'member' must be type discord.Member")

        await super()._create_record(self.__table[0], {
            "discord_id": member.id,
            "university_id": "null",
            "xp_level": 0,
            "elo_rating": 0,
            "bot_level": 0,
            "about_me": "none"
        })

    async def check_if_member_record_exists(self, discord_id: int):
        if not isinstance(discord_id, int):
            print("'guild_id' must be int, not any other type.")

        query_result = await super()._read_record(self.__table[0], discord_id)

        if len(query_result) != 0:
            return True

        return False

    async def get_record(self, discord_id: int) -> Member:
        """
        Returns a copy of the record in the form of a Member dataclass.\n
        At the moment any changes to an instance of Member, will not affect the database.\n
        This function it's mostly used for testing purposes, if you want to see the values of this record you should
        use the property from the Member dataclass:\n
        *Example*:
            `member = await members_dao.get_record(4545)` \n
            `member.info`

        Returns:
            - An instance of the Member dataclass
        """
        async with self.__connection_pool.acquire() as connection:
            record = await connection.fetchrow(
                f"""
                    SELECT * FROM {self.__table[0]} WHERE discord_id = $1
                """,
                discord_id)

            # Converts the record fetched into a Member Dataclass
            return Member(record['discord_id'], record['university_id'],
                          record['xp_level'], record['elo_rating'],
                          record['bot_level'], record['about_me'])

    async def update_field(self, discord_id: int, attribute: Member.Enum, value: int) -> None:
        """
        Updates a field within a RECORD. \n
        This function is responsible for changing only one value within the parsed primary_key \n

        Note: This is the opposite of the super class update_record. \n
        
        :param discord_id: the user whose field will be updated
        :param attribute: the attribute that needs to be changed
        :param value: the updated value that will be committed to database
        """
        # Pre-check to make sure attribute is correct type
        if not isinstance(attribute, Member.Enum):
            print("Unknown 'attribute' type, please use only Member.Enum types.")
            return

        # Discord ID cannot be updated, as it does not change
        if attribute == "discord_id":
            print("Updating 'discord_id' cannot be done for the database, it is not allowed.")
            return

        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {self.__table[0]}
                SET {attribute} = $2
                WHERE discord_id = $1
                """,
                discord_id,
                value
            )

            connection.close()

    async def update_member_university_id(self, member_id: int, new_university_id: str):

        if not isinstance(new_university_id, str):
            print("Please give in an string value for 'new_university_id'!")
            return None

        if len(new_university_id) > 8 or len(new_university_id) < 8:
            print("'university_id' takes in value of length 8, value given was not '8' in length.")
            return None

        if new_university_id[0] != 'w':
            print("University ID begins with 'w', it was not found in the value given.")
            return None

        await super()._update_record(self.__table[0], member_id, {"university_id": new_university_id})

    async def update_member_xp_level(self, member_id: int, new_xp_level: int):
        await super()._update_record(self.__table[0], member_id, {"xp_level": new_xp_level})

    async def update_member_elo_level(self, member_id: int, new_elo_rating: int):
        await super()._update_record(self.__table[0], member_id, {"elo_rating": new_elo_rating})

    async def update_member_bot_level(self, member_id: int, new_bot_level: int):
        await super()._update_record(self.__table[0], member_id, {"bot_level": new_bot_level})

    async def update_member_about_me(self, member_id: int, new_about_me: str):
        await super()._update_record(self.__table[0], member_id, {"about_me": new_about_me})

    async def commit(self, member: Member):
        """
        Updates the database Record with information from the Member object. \n
        Any changes made to the Member class has to be committed through this function.
        """
        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {self.__table[0]}
                SET university_id = $2, xp_level = $3, elo_rating = $4, bot_level = $5, about_me = $6
                WHERE discord_id = $1
                """,
                member.discord_id,
                member.university_id,
                member.xp_level,
                member.elo_rating,
                member.bot_level,
                member.about_me
            )
