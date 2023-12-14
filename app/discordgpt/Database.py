import asyncpg

class ImageDatabase:
    """
    Database class using the asyncpg PostgreSQL Driver
    """
    def __init__(self, **kwargs):
        self.pg_username = kwargs.get("pg_username")
        self.pg_password = kwargs.get("pg_password")
        self.pg_database = kwargs.get("pg_db")
        self.pg_host = kwargs.get("pg_host")

    async def create_user(self, username: str):
        """
        Create a new user in the database
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        await conn.execute('''
            INSERT INTO Users (Username)
            VALUES ($1)''', username)

        await conn.close()

    async def store_generated_image(self, b2_filename: str, username: str, prompt: str, caption: str):
        """
        Store a reference to the generated image in the Boggart database
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        username_from_db = await conn.fetchval('SELECT UserID FROM Users WHERE Username = $1', username)

        if username_from_db:
            await conn.execute('''
                INSERT INTO GeneratedImages (ImageLink, TimeCreated, UserID, Prompt, Caption)
                VALUES ($1, CURRENT_TIMESTAMP AT TIME ZONE 'UTC', $2, $3, $4)
            ''', b2_filename, username_from_db, prompt, caption)
        else:
            raise Exception("Error inserting image into database")

        await conn.close()

    async def get_all_users(self):
        """
        Returns a list of all users
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
            
        data = await conn.fetch('SELECT * FROM Users')

        for r in data:
            print(f"{r['username']}: {r['userid']}")

        await conn.close()

    async def get_all_images(self):
        """
        Return a list of all database records of all images
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        data = await conn.fetch('SELECT * FROM GeneratedImages')

        for r in data:
            print(f"UserID: {r['userid']} - Image Link: {r['imagelink']}\nTime Created: {r['timecreated']}\nPrompt: {r['prompt']}\nCaption {r['caption']}\n")

        await conn.close()

    async def get_all_user_images(self, username:str):
        """
        Return a list of all images generated by a given user

        Arguments:
        - `username`
        """
        conn = await asyncpg.connect(user=self.pg_username,
                                     password=self.pg_password,
                                     database=self.pg_database,
                                     host=self.pg_host)
        
        data = await conn.fetch('''
            SELECT U.Username, G.ImageLink, G.TimeCreated, G.Caption
            FROM GeneratedImages G
            INNER JOIN Users U on G.UserID = U.UserID
            WHERE U.Username = $1''', username)

        await conn.close()

        return data