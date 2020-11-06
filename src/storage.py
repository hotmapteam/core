from simple_settings import settings
import motor.motor_asyncio
import typing
from model import Message

client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
db = client[settings.DB_NAME]
collection = db.messages


async def write(messages: typing.List[Message]):
    collection.insert_many([m.__dict__ for m in messages])
