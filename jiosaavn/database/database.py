import datetime
import motor.motor_asyncio
 
 
class Database:
    
    def __init__(self, uri):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.user_db = self._client['jiosaavn_users']
        self.id_db = self._client['jiosaavn_ids']
        self.col = self.user_db.users
        self.id_col = self.id_db.ids
    
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat(),
            type="all",
            ban_status={
                'is_banned': False,
                'ban_duration': 0,
                'banned_on': datetime.date.max.isoformat(),
                'ban_reason': ''
            }
        )
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':id})
        return True if user else False

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    async def get_type(self, id):
        user = await self.col.find_one({'id':id})
        type = user.get('type')
        return type

    async def update_type(self, id, value):
        await self.col.update_one({'id': id}, {'$set': {'type': value}})   

    async def is_id_exist(id):
        song = await self.id_col.find_one({'id': id})
        self.id_col.insert_one({id: id, song: []})
        return True if song else False

    async def get_song(id):
        song = await self.id_col.find_one({'id': id})
        song_ids = song.get('song')
        return song_ids

    async def update_song(id, song):
        song = await self.id_col.find_one({'id': id})

