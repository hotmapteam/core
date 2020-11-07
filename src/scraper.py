import telegram
import asyncio
import storage
import logging
import argparse
import classificator

from geopy.geocoders import Nominatim as Geolocator


async def scrap():
    async for feed in storage.Feed.find():
        logging.debug("feed %r", feed)
        if feed.type == "telegram":
            async for message in telegram.list_messages(int(feed.uri)):
                logging.debug("message %r", message)

                classification_spans = classificator.classificate(message.raw_text)

                org = classification_spans.get("ORG", None)
                address = classification_spans.get("LOC", None)

                if not address and org:
                    address = org
                else:
                    address = "Минск, Беларусь"

                # Use OpenStreetMaps API to resolve geococde address
                location = Geolocator().geocode(address)

                a = storage.Article(
                    text=message.raw_text,
                    date=message.date,
                    source=feed,
                    location={
                        "type": "Point",
                        "location": {
                            "coordinates": [location.latitude, location.longitude]
                        },
                    },
                    address=location.address,
                )
                await a.commit()


async def add_feed(type: str, uri: str):
    f = storage.Feed(type=type, uri=uri)
    await f.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--add-feed", type=str, help="add feed <type,uri>")
    args = parser.parse_args()

    if type(args.add_feed) is str:
        asyncio.get_event_loop().run_until_complete(add_feed(*args.add_feed.split(",")))
    else:
        logging.info("starting scrapper")
        asyncio.get_event_loop().run_until_complete(scrap())
