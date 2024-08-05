import datetime
import motor.motor_asyncio

class Database:
    def __init__(self, uri: str):
        """
        Initializes the Database instance with the provided URI.

        Args:
            uri (str): The MongoDB URI.
        """
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.user_db = self._client['jiosaavnV2_users']
        self.id_db = self._client['jiosaavnV2_ids']
        self.user_collection = self.user_db.users
        self.id_collection = self.id_db.ids

    @staticmethod
    def new_user(user_id: int) -> dict:
        """
        Creates a new user dictionary with default values.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            dict: The user dictionary.
        """
        return {
            'id': user_id,
            'join_date': datetime.date.today().isoformat(),
            'type': 'all',
            'quality': '320kbps',
            'ban_status': {
                'is_banned': False,
                'ban_duration': 0,
                'banned_on': datetime.date.max.isoformat(),
                'ban_reason': ''
            }
        }

    async def is_user_exist(self, user_id: int) -> bool:
        """
        Checks if a user exists in the database.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user = await self.user_collection.find_one({'id': user_id})
        return bool(user)

    async def add_user(self, user_id: int):
        """
        Adds a new user to the database.

        Args:
            user_id (int): The unique identifier for the user.
        """
        user = self.new_user(user_id)
        await self.user_collection.insert_one(user)
        return user

    async def get_user(self, user_id: int) -> dict:
        """
        Retrieves a user from the database.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            dict: The user document from the database.
        """
        user = await self.user_collection.find_one({'id': user_id})
        if not user:
            user = await self.add_user(user_id)
        return user

    async def update_user(self, user_id: int, key: str, value: any):
        """
        Updates a user's information in the database.

        Args:
            user_id (int): The unique identifier for the user.
            key (str): The key to update.
            value (any): The value to set for the key.
        """
        await self.user_collection.update_one({'id': user_id}, {'$set': {key: value}})

    async def is_song_id_exist(self, item_id: str) -> bool:
        """
        Checks if an song ID exists in the database.

        Args:
            item_id (str): The unique identifier for the item.

        Returns:
            bool: True if the ID exists, False otherwise.
        """
        item = await self.id_collection.find_one({'id': item_id})
        if not item:
            await self.id_collection.insert_one({'id': item_id, 'chat_id': 0, 'message_id': 0})
        return bool(item)

    async def get_song(self, song_id: str) -> dict:
        """
        Retrieves a song from the database.

        Args:
            song_id (str): The unique identifier for the song.

        Returns:
            dict: The song document from the database.
        """
        song = await self.id_collection.find_one({'id': song_id})
        return song

    async def update_song(self, song_id: str, quality: str, chat_id: int, message_id: int):
        """
        Updates a song's information in the database.

        Args:
            song_id (str): The unique identifier for the song.
            quality (str): The quality of the song (e.g., '320kbps').
            chat_id (int): The chat ID.
            message_id (int): The message ID.
        """
        update_fields = {
            f'{quality}.chat_id': chat_id,
            f'{quality}.message_id': message_id
        }
        await self.id_collection.update_one({'id': song_id}, {'$set': update_fields})
