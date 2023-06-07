import asyncio
import asyncpg

from GuildsDAO import GuildsDAO
from MembersDAO import MembersDAO
# from Members import Member


async def main():
    connection_pool = await asyncpg.create_pool(
        database="mydatabase", user="myuser", password="", command_timeout=10
    )

    # Creates a dao object to interact with the database
    members_dao = MembersDAO(connection_pool, "members")
    guilds_dao = GuildsDAO(connection_pool, "guilds")

    # if you want to create a record:
    # await members_dao.create_member(20202020,"w1234567", 0, 0, 1)

    # view the user
    print("User Card")
    memberObj = await members_dao.get_record(20202020)
    # returns you the "user card" as I call it
    print(await memberObj.info)

    print(await memberObj.info_tuple)

    # await members_dao.update_field(memberObj.discord_id, Member.Enum.XP_LEVEL, 1000)
    # memberObj = await members_dao.get_record(20202020)
    # print(await memberObj.info)

    # print("All records")
    # # basic example
    # records = await members_dao.get_all_records
    #
    # # print all records
    # for record in records:
    #     print(record)

    await guilds_dao.set_up()

    await guilds_dao.create_guild(1000001, "help")


asyncio.run(main())
