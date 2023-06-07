from datetime import datetime

from AbstractDAO import AbstractDAO


class GuildsDAO(AbstractDAO):
    # Current problem with this class is that its inheriting from abstractdao and
    # the variables there are written for membersdao so there is that.
    def __init__(self, connection_pool, table_name):
        super().__init__(table_name,
                         "(guild_id, description, created_at, joined_at, members_count, owner_id)",
                         connection_pool)
        self.connection_pool = connection_pool

    async def set_up(self):

        # NOTE(nuke): this needs to be moved out of the DAOs and into a preliminary file
        # that gets run at start of runtime, ie 'on_ready' in Emperor.py
        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS guilds (
                    guild_id 	bigint NOT NULL,
                    description	text,
                    created_at	DATE NOT NULL,
                    joined_at   DATE NOT NULL,
                    members_count int NOT NULL,
                    owner_id    int NOT NULL
                )
                """
            )

    async def create_guild(self, guild_id: int, description: str = "none"):
        # NOTE(nuke): values are hardcoded for demonstration, in future argument of discord.Guild
        # will be passed that replaces the hardcoded values
        await super()._create(guild_id, description, datetime.now().date(), datetime.now().date(), 1, 1023993023)
