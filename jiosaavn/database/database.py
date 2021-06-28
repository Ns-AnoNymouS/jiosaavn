import datetime
import motor.motor_asyncio
 
 
class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
    
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat(),
            settings="all",
            ban_status={
                'is_banned': False,
                'ban_duration': 0,
                'banned_on': datetime.date.max.isoformat(),
                'ban_reason': ''
            }
        )
    

################## Checking & Adding New User 👤 ##################

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':id})
        return True if user else False


    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
