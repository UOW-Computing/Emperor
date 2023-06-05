from Members import Member
from AbstractDAO import AbstractDAO


class MembersDAO(AbstractDAO):
    """
    MembersDAO class is responsible for acting as the API between Emperor and its Database.\n
    Any changes to the users of the database should be done through MembersDAO not AbstractDAO.
            Functions
        - create_member()       - Creates a record
        - delete_member()       - Deletes a record
        - update_record()       - Master update all field in a record
        - get_record()          - Returns a Record as a Member Dataclass
        - update_field()        - Change a specific field
        - commit()              - Pushes changes from a Member class to the Database
        \n

        Properties(Getters)
            - get_all_records   - Returns all records within the table
            - get_field         - Returns a specific field from the parsed column
     """

    def __init__(self, connection_pool, table_name, columns_names):
        """

        :param connection_pool: Inherited connection pool from AbstractDAO
        :param table_name:      table_name corresponds the table in the database
        :param columns_names:   columns within the table
        """
        super().__init__(table_name, columns_names, connection_pool)
        self.connection_pool = connection_pool

    async def get_record(self, discord_id: int) -> Member:
        """ Returns a copy of the record in the form of a Member dataclass.\n
        At the moment any changes to an instance of Member, will not affect the database.\n
        This function it's mostly used for testing purposes, if you want to see the values of this record you should
        use the property from the Member dataclass:\n
        *Example*:
            `member = await members_dao.get_record(4545)` \n
            `member.info`

        Returns:
             - An instance of the Member dataclass
        """
        async with self.connection_pool.acquire() as connection:
            record = await connection.fetchrow(
                f"""
                    SELECT * FROM {self.table_name} WHERE discord_id = $1
                    """,
                discord_id)

            # Converts the record fetched into a Member Dataclass
            return Member(record['discord_id'], record['university_id'],
                          record['xp_level'], record['elo_rating'],
                          record['bot_level'], record['about_me'])

    async def update_field(self, discord_id: int, attribute_to_change: str, value_to_change: int) -> None:
        """ Updates a field within a RECORD. \n
        This function is responsible for changing only one value within the parsed primary_key \n

        Note: This is the opposite of the super class update_record. \n
        """
        async with self.connection_pool.acquire() as connection:
            if attribute_to_change == 'university_id':
                await connection.execute(
                    f"""
                    UPDATE {self.table_name}
                    SET university_id = $2
                    WHERE discord_id = $1
                    """,
                    discord_id,
                    value_to_change
                )
            elif attribute_to_change == 'xp_level':
                await connection.execute(
                    f"""
                    UPDATE {self.table_name}
                    SET xp_level = $2
                    WHERE discord_id = $1
                    """,
                    discord_id,
                    value_to_change
                )
            elif attribute_to_change == 'elo_rating':
                await connection.execute(
                    f"""
                    UPDATE {self.table_name}
                    SET elo_rating = $2
                    WHERE discord_id = $1
                    """,
                    discord_id,
                    value_to_change
                )
            elif attribute_to_change == 'bot_level':
                await connection.execute(
                    f"""
                    UPDATE {self.table_name}
                    SET bot_level = $2
                    WHERE discord_id = $1
                    """,
                    discord_id,
                    value_to_change
                )

    async def commit(self, member: Member):
        """Updates the database Record with information from the Member object. \n
        Any changes made to the Member class has to be committed through this function.
            """
        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {self.table_name}
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
