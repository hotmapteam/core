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


async def scrap():
    async for feed in storage.Feed.find():
        logging.debug("feed %r", feed)
        max_ts = feed.last_ts

        try:
            if feed.type == "telegram":
                async for message in telegram.list_messages(int(feed.uri)):

                    if feed.last_ts >= message.date.timestamp():
                        logging.debug(f"{feed.type}://{feed.uri} is up to date")
                        break

                    max_ts = max(max_ts, message.date.timestamp())
                    classification_spans = classificator.classificate(message.raw_text)

                    org = classification_spans.get("ORG", None)
                    address = classification_spans.get("LOC", None)

                    if not address and org:
                        address = org
                    else:
                        address = "Минск, Беларусь"

                    while True:
                        try:
                            # OpenStreetMaps geocoding
                            location = Geolocator(user_agent="hotmap").geocode(address)
                            break
                        except geopy.exc.GeocoderServiceError:
                            retry_timeout = random.randint(3, 10)
                            logging.warning(
                                "GeocoderServiceError, retrying in %d seconds",
                                retry_timeout,
                            )
                            await asyncio.sleep(retry_timeout)

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

                    logging.debug(
                        "message %r %r %r", message, a.dump(), classification_spans
                    )
                    await a.commit()

        finally:
            feed.last_ts = max_ts
            await feed.commit()


async def add_feed(type: str, uri: str):
    f = storage.Feed(type=type, uri=uri)
    await f.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--add-feed", type=str, help="add feed <type,uri>")
    parser.add_argument("--forever", type=int, help="run forever")
    args = parser.parse_args()

    if type(args.add_feed) is str:
        asyncio.get_event_loop().run_until_complete(add_feed(*args.add_feed.split(",")))
    else:
        logging.info("starting scrapper")

        while args.forever:
            asyncio.get_event_loop().run_until_complete(scrap())
            time.sleep(args.forever)
        else:
            asyncio.get_event_loop().run_until_complete(scrap())
