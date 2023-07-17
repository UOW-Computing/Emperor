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
from asyncpg import Record
from typing import Any


class AbstractDAO:
    """
    An informal abstract Class used to represent a Data Access Object. All methods within this class can be passed
    down to subclasses and perform respectively to their initial purpose. This class is inherited by every database
    table class.

    :author: Breno

    """

    def __init__(self, connection_pool):
        """
        Initialised the object with connection pool, creating a reference to the AbstractDAO object.
        """
        self.__connection_pool = connection_pool

        super(AbstractDAO, self).__init__()

    # Old versions
    # async def create_member(self, discord_id, university_id, xp_level, elo_rating, bot_level):
    #     """Create a record within the table.\n
    #     Currently no error handling added.
    #     """
    #     async with self.connection_pool.acquire() as connection:
    #         await connection.execute(
    #             f"""
    #             INSERT INTO {self.table_name} {self.columns_names}
    #             VALUES ($1, $2, $3, $4, $5)
    #             """,
    #             discord_id,
    #             university_id,
    #             xp_level,
    #             elo_rating,
    #             bot_level)
    #
    # async def delete_member(self, discord_id: int):
    #     """
    #     DELETES the record from the table
    #     :param discord_id: int ID of the user to be deleted
    #     """
    #     async with self.connection_pool.acquire() as connection:
    #         await connection.execute(
    #             f"""
    #             DELETE FROM {self.table_name} WHERE discord_id = $1
    #             """,
    #             discord_id
    #         )
    #
    # async def update_record(self, table_name, discord_id, university_id, xp_level, elo_rating, bot_level):
    #     """Master update function\n
    #     This function requires all 5 fields to be updated. \n
    #     If you want to update just one field, use update_field from the subclass instead.
    #
    #     *Example:* \n
    #     update_record(primary_key, user_id, 1000, 1000, 1)
    #     """
    #     async with self.connection_pool.acquire() as connection:
    #         await connection.execute(
    #             f"""
    #             UPDATE {table_name}
    #             SET university_id = $2, xp_level = $3, elo_rating = $4, bot_level = $5
    #             WHERE discord_id = $1
    #             """,
    #             discord_id,
    #             university_id,
    #             xp_level,
    #             elo_rating,
    #             bot_level
    #         )

    ######################################
    #
    #           Helper Functions
    #
    ######################################

    async def __get_primary_key_column(self, table_name: str) -> str:
        """
        Gets a Primary Key of the table.
        
        :param table_name: str The name of the table its being queried for
        
        :return: str Primary key of the table

        """
        async with self.__connection_pool.acquire() as connection:
            pk = await connection.fetchval(
                f"""
                    SELECT a.attname
                    FROM pg_constraint c
                    JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
                    WHERE c.conrelid = '{table_name}'::regclass
                    AND c.contype = 'p'
                    LIMIT 1;
                    """
            )

        return pk

    ######################################
    #                                    #
    #            CRUD METHODS            #
    #                                    #
    ######################################

    async def _create_record(self, table_name: str, columns: dict) -> bool:
        """
            Creates a record.


            It can create a record by giving in the values through a dictionary.
            Where each key relates to the columns and the value being the columns value.
            Order of the columns matter, therefore follow the value it is listed in the database.

            Example::

                data = {
                    "column_1": "string_value",
                    "column_2": 50,
                }
                await ref._create_record("table", data)

            NOTE:
                Deleting this record, without deleting any other linked records will result in
                them being deleted. Therefore, be aware of unintended consequences.

            :param str table_name: The table in which the record is being inserted.
            :param dict columns: Dictionary holding all the data, with its keys being the column names.

            :return: True on record creation, False on failure.

        """

        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                    INSERT INTO {table_name} ({', '.join([f'{k}' for k in columns.keys()])})
                    VALUES ({', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in columns.values()])})
                    ON CONFLICT DO NOTHING;
                """
            )

            return True

    async def _read_record(self, table_name: str, key: int, limit: int = 1) -> Record | list[Record]:
        """
            Reads a record.


            Using the key to search the table, it finds the record(s) then returns the record(s),
            depending on the limit.

            **Example**::

                await ref._read_record("table", 1)
                await ref._read_record("table", 3, 100)

            :param str table_name: the table in which the record is read from.
            :param int key: the identifier for the record in the table.
            :param int limit: the amount of records to return from the query, Defaults to 1.

            :return: list of queried records or single queried record. None on no records found


        """

        async with self.__connection_pool.acquire() as connection:
            query = await connection.fetch(
                f"""
                SELECT * FROM {table_name}
                WHERE {await self.__get_primary_key_column(table_name)} = {key}
                LIMIT {limit};
                """
            )

            return query[0] if (len(query) == 1) else query

    async def _update_record(self, table_name: str, key: int, columns: dict) -> bool:
        """
            Updates a record.


            It can update single or multiple columns, depending on the dictionary being given in.
            Using the dictionary, each key can relate to the different columns inside the table, and the
            values correspond to the values for the columns.


            NOTE: The table needs to have a primary key defined before the function can work. It
            relies on the primary key to set value.


            Example::

                data = {
                    "column_1": 5,
                     "column_2": "a new string"
                }
                await ref._update_record("table", 1, data)

            :param str table_name: name of the table for updating record
            :param int key: the identifier of the record, that needs to be updated
            :param dict columns: columns with their new value that need to be updated.

            :return: True if the record was updated, False if not

        """

        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {table_name}
                SET {", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in columns.items()])}
                WHERE {await self.__get_primary_key_column(table_name)} = {key};
                """
            )
            return True

    async def _delete_record(self, table_name: str, key: int) -> bool:
        """
            Deletes a record.

            Using the key provided, it looks through the table and deletes the record.


            NOTE: As you delete the record, all other records in the same or other tables that rely on this record
            may be deleted.

            **Example**::

                await ref._delete_record("table", 1)

            :param table_name: str Name of the table where the record is located
            :param key: int The identifier for the record, in most cases the primary key.

            :return: True, if the record was deleted. False if it was not deleted.

        """

        async with self.__connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                DELETE FROM {table_name}
                WHERE {await self.__get_primary_key_column(table_name)} = {key}
                """
            )

            return True

    async def _get_column_record(self, table_name: str, column_name: str, primary_key: int) -> Any:
        """
        Returns the searched value in the table.\n

        :param table_name: name of the table
        :param primary_key: discord_id / guild_id
        :param column_name: table name / search value

        Example:
            TO DO
        """
        async with self.__connection_pool.acquire() as connection:
            result = await connection.fetchval(
                f"""
                SELECT {column_name}
                FROM {table_name}
                WHERE {await self.__get_primary_key_column(table_name)} = {primary_key}
                """
            )
            return result

    async def _get_all_records(self, table_name) -> list[Record]:
        """
        Returns all records within the table. \n

        *Currently not formatted*.
        """
        async with self.__connection_pool.acquire() as connection:
            result = await connection.fetch(
                f"""
                SELECT * FROM {table_name}
                """
            )

            return result
