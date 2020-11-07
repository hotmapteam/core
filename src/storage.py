from simple_settings import settings
import motor.motor_asyncio
from umongo import Instance, Document, fields

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
    date = fields.DateTimeField(required=True)
    text = fields.StringField()
    tags = fields.ListField(fields.StringField(), default=[])
    source = fields.ReferenceField("Feed")
    address = fields.StringField(default="")
    # Location: {
    #       type: "Point",
    #       coordinates: [-73.856077, 40.848447]
    # }
    location = fields.DictField(default={})

    class Meta:
        collection_name = "article"
