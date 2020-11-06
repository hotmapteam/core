from simple_settings import settings
import motor.motor_asyncio
import datetime as dt
from umongo import Instance, Document, fields, validate

client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
db = client[settings.DB_NAME]
odb = Instance(db)


@odb.register
class Feed(Document):
    type = fields.StringField()
    uri = fields.StringField()

    class Meta:
        collection_name = "feed"


@odb.register
class Article(Document):
    date = fields.DateTimeField(validate=validate.Range(min=dt.datetime(1900, 1, 1)))
    text = fields.StringField()
    tags = fields.ListField(fields.StringField())
    source = fields.ReferenceField("Feed")
    address = fields.StringField()
    location = fields.ListField(fields.FloatField())

    class Meta:
        collection_name = "article"
