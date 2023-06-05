import asyncio
import asyncpg

from GuildsDAO import GuildsDAO
from MembersDAO import MembersDAO


async def main():
    connection_pool = await asyncpg.create_pool(
        database="mydatabase", user="myuser", password="", command_timeout=10
    )

    # Creates a dao object to interact with the database
    members_dao = MembersDAO(connection_pool, "members", "(discord_id, university_id, xp_level, elo_rating, bot_level)")
    guilds_dao = GuildsDAO(connection_pool, "guilds", "(guild_id, description, created_at, joined_at, members_count, "
                                                      "owner_id, log_channels, staff_roles)")

    # if you want to create a record:
    # await members_dao.create_member(20202020,"w1234567", 0, 0, 1)

    # view the user
    print("User Card")
    memberObj = await members_dao.get_record(20202020)
    # returns you the "user card" as i call it
    print(await memberObj.info)



    print()
    print("All records")
    # basic example
    records = await members_dao.get_all_records

    # print all records
    for record in records:
        print(record)


asyncio.run(main())
