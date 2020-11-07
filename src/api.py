from sanic import Sanic, response
from sanic.request import Request
from sanic_cors import CORS
from simple_settings import settings
import asyncio
import storage


app = Sanic(__name__)
CORS(app)


async def get_model(request: Request, model: storage.Document):
    filt = request.args.copy()
    skip = filt.pop("skip", 0)
    limit = filt.pop("limit", 0)

    return response.json(await model.find(filt).skip(skip).limit(limit).to_list(None))


@app.route("/api/v1/article", methods=["GET", "OPTIONS"])
async def list_articles(request: Request):
    return await get_model(request, storage.Article)


@app.route("/api/v1/feed", methods=["GET", "OPTIONS"])
async def list_feeds(request: Request):
    return await get_model(request, storage.Feed)


if __name__ == "__main__":
    asyncio.ensure_future(
        app.create_server(
            host=settings.API_LISTEN[0],
            port=settings.API_LISTEN[1],
            return_asyncio_server=True,
        )
    )
    asyncio.get_event_loop().run_forever()
