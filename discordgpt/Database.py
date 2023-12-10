import asyncpg

class Database:
    def __init__(self, **kwargs):
        self.pg_username = kwargs.get("pg_username")
        self.pg_password = kwargs.get("pg_password")
        self.pg_database = kwargs.get("pg_db")
        self.pg_host = kwargs.get("pg_host")

    async def create_db_structure(self):
        """
        Create the Boggart database structure
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        # create_uuid_extension
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

        # create "Users" table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                Username VARCHAR(255) UNIQUE NOT NULL,
                LastUploadTime TIMESTAMPTZ,
                ImagesCreated INT DEFAULT 0
            )
        ''')

        # create the "GeneratedImages" table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS GeneratedImages (
                ImageID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                Link VARCHAR(255) NOT NULL,
                TimeCreated TIMESTAMPTZ NOT NULL,
                UserID UUID NOT NULL,
                Prompt TEXT NOT NULL,
                Caption TEXT NOT NULL,
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )
        ''')

        await conn.close()

    async def create_user(self, username: str):
        """
        Create a new user in the database
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        await conn.execute('''
            INSERT INTO Users (Username, LastUploadTime, ImagesCreated)
            VALUES ($1, CURRENT_TIMESTAMP AT TIME ZONE 'UTC', 0)''', username)

        await conn.close()

    async def store_generated_image(self, b2_link: str, username: str, prompt: str, caption: str):
        """
        Store a reference to the generated image in the Boggart database
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        username_from_db = await conn.fetchval('SELECT UserID FROM users WHERE username = $1', username)

        if username_from_db:
            await conn.execute('''
                INSERT INTO GeneratedImages (Link, TimeCreated, UserID, Prompt, Caption)
                VALUES ($1, CURRENT_TIMESTAMP AT TIME ZONE 'UTC', $2, $3, $4)
            ''', b2_link, username_from_db, prompt, caption)
        else:
            raise Exception("Error inserting image into database")

        await conn.close()

# TODO: get image links
# TODO: get a list of image links