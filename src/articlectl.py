import telegram
import asyncio
import storage
import logging
import argparse
import classificator
import time
import random

import geopy
from geopy.geocoders import Nominatim as Geolocator

logger = logging
geocode_cache = dict()


async def geocode(address: str):
    if address in geocode_cache:
        return geocode_cache[address]
    else:
        while True:
            try:
                # OpenStreetMaps geocoding
                location = Geolocator(user_agent="hotmap").geocode(address)
                geocode_cache[address] = location
                return location
            except geopy.exc.GeocoderServiceError:
                retry_timeout = random.randint(3, 10)
                logger.warning(
                    "GeocoderServiceError, retrying in %d seconds",
                    retry_timeout,
                )
                await asyncio.sleep(retry_timeout)


async def segmentate(text: str):
    classification_spans = classificator.segmentate(text)
    logger.info("segmentate() %s: %r", text, classification_spans)
    extracted_org = classification_spans.get("ORG", "")
    extracted_address = classification_spans.get("LOC", "")
    full_address = f"{extracted_address}, {extracted_org}"
    location = await geocode(full_address)
    return location


async def scrap():
    async for feed in storage.Feed.find():
        logger.debug("feed %r", feed)
        max_ts = feed.last_ts

        try:
            if feed.type == "telegram":
                async for message in telegram.list_messages(int(feed.uri)):

                    if feed.last_ts >= message.date.timestamp():
                        logger.debug(f"{feed.type}://{feed.uri} is up to date")
                        break

                    max_ts = max(max_ts, message.date.timestamp())
                    location = await segmentate(message.text)

                    a = storage.Article(
                        text=message.raw_text,
                        ts=message.date.timestamp(),
                        source=feed,
                        location={
                            "type": "Point",
                            "location": {
                                "coordinates": [location.latitude, location.longitude]
                            },
                        },
                        address=location.address,
                    )

                    logger.debug("article: %r", a.dump())
                    await a.commit()

        finally:
            feed.last_ts = max_ts
            await feed.commit()


async def add_feed(type: str, name: str, uri: str):
    f = storage.Feed(type=type, name=name, uri=uri)
    await f.commit()


async def resegmentate():
    async for a in storage.Article.find():
        location = await segmentate(a.text())
        a.location["location"]["coordinates"] = location
        logger.info(a.dump())
        await a.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logger.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--add-feed", type=str, help="add feed <type,name,uri>")
    parser.add_argument(
        "--resegmentate",
        action="store_true",
        help="reclassificate articles in the database",
    )
    parser.add_argument(
        "--fetch", action="store_true", help="fetch articles from feeds"
    )
    parser.add_argument("--forever", type=int, help="run forever")
    args = parser.parse_args()

    if type(args.add_feed) is str:
        asyncio.get_event_loop().run_until_complete(add_feed(*args.add_feed.split(",")))
    elif args.resegmentate:
        asyncio.get_event_loop().run_until_complete(resegmentate())
    elif args.fetch:
        logger.info("fetching articles...")

        while args.forever:
            asyncio.get_event_loop().run_until_complete(scrap())
            time.sleep(args.forever)
        else:
            asyncio.get_event_loop().run_until_complete(scrap())
