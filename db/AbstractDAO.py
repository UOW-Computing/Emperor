class AbstractDAO:
    """
    An informal abstract Class used to represent a Data Access Object. \n


    Attributes:
        table_name (str): Responsible for accessing/representing the table name within the connected database.

        columns_names (str): Represents the columns within the table.

    - ALL the methods within this class can be passed down to subclasses and perform respectively to their initial purpose.
    - This class is inherited by every database table class, Members, Guild etc.. \n
    """
    table_name: str
    columns_names: str
    num_of_records: int

    def __init__(self, table_name, columns_names, connection_pool):
        """ Initialised the object with values that correspond to the table and column names of the database."""
        self.table_name = table_name
        self.columns_names = columns_names
        self.connection_pool = connection_pool

    async def create_member(self, discord_id, university_id, xp_level, elo_rating, bot_level):
        """Create a record within the table.\n
        Currently no error handling added.
        """
        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                INSERT INTO {self.table_name} {self.columns_names}
                VALUES ($1, $2, $3, $4, $5)
                """,
                discord_id,
                university_id,
                xp_level,
                elo_rating,
                bot_level
            )

    async def _create(self, *columns):
        """
            Abstracted version and backbone of create_guild, create_member.\n
            All error handling should be done in create_guild and create_member
        """

        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                    INSERT INTO {self.table_name} {self.columns_names}
                    VALUES ({', '.join(['${}'.format(i) for i in range(1, len(columns) + 1)])})
                    """,
                *columns
            )

    async def delete_member(self, discord_id: int):
        """DELETES the record from the table
        :param discord_id: int"""
        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                DELETE FROM {self.table_name} WHERE discord_id = $1
                """,
                discord_id
            )

    async def update_record(self, discord_id, university_id, xp_level, elo_rating, bot_level):
        """Master update function\n
        This function requires all 5 fields to be updated. \n
        If you want to update just one field, use update_field from the subclass instead.

        *Example:* \n
        update_record(primary_key, user_id, 1000, 1000, 1)
        """
        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {self.table_name}
                SET university_id = $2, xp_level = $3, elo_rating = $4, bot_level = $5
                WHERE discord_id = $1
                """,
                discord_id,
                university_id,
                xp_level,
                elo_rating,
                bot_level
            )

    async def get_field(self, primary_key: int, column_name: str):
        """Returns the searched value
        :param primary_key: discord_id / guid_id
        :param column_name: table name / search value

        Example:
            get_field(4545, "xp_level") -> 4545 : xp_level = 10000
        """
        async with self.connection_pool.acquire() as connection:
            result = await connection.fetchval(
                f"""
                SELECT {column_name}
                FROM {self.table_name}
                WHERE discord_id = $1
                """,
                primary_key
            )
            return result

    @property
    async def get_all_records(self):
        """ Returns all records within the table. \n

        *Currently not formatted*."""
        async with self.connection_pool.acquire() as connection:
            result = await connection.fetch(
                f"""
                SELECT * FROM {self.table_name}
                """
            )
            return result
