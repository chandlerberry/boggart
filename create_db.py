import asyncio
import asyncpg
import discordgpt

async def get_all_users():
    conn = await asyncpg.connect(user='postgres', password='chandlerb', 
                                 database='postgres', host='127.0.0.1')
    
    data = await conn.fetch('SELECT * FROM Users')

    print(data)

    await conn.close()

async def main():

    db = discordgpt.Database(pg_username='postgres',
                  pg_password='chandlerb',
                  pg_db='postgres',
                  host='127.0.0.1:5432')
    
    await db.create_db_structure()
    
    # await db.create_user("user1")
    # await db.create_user("user2")
    # await db.create_user("user3")

    # TODO: image upload tests

    await get_all_users()

asyncio.run(main())