from AbstractDAO import AbstractDAO


class GuildsDAO(AbstractDAO):
    # Current problem with this class is that its inheriting from abstractdao and
    # the variables there are written for membersdao so there is that.
    def __init__(self, connection_pool, table_name, columns_names):
        super().__init__(table_name, columns_names, connection_pool)
        self.connection_pool = connection_pool

    async def set_up(self):
        async with self.connection_pool.acquire() as connection:
            await connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS guilds (
                    guild_id 	bigint NOT NULL,
                    description	text,
                    members		int NOT NULL,
                    created_at	DATE NOT NULL,
                    owner_id    int NOT NULL
        
                )
                """
            )
