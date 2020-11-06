import telegram
import asyncio
import storage
import logging
import argparse


async def scrap():
    async for feed in storage.Feed.find():
        logging.debug("feed %r", feed)
        if feed.type == "telegram":
            async for message in telegram.list_messages(int(feed.uri)):
                logging.debug("message %r", message)
                a = storage.Article(text=message.raw_text, date=message.date)
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
