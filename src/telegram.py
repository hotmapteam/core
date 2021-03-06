import argparse
from telethon import TelegramClient
from simple_settings import settings

client = TelegramClient(
    settings.TELEGRAM_SESSION_NAME, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH
)


async def list_messages(dialog_id):
    async with client:
        async for message in client.iter_messages(dialog_id):
            yield message


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--list-dialogs", action="store_true", help="list chats and channels"
    )
    parser.add_argument("--list-messages", type=int, help="list messages")
    args = parser.parse_args()

    if args.list_dialogs:
        async for dialog in client.iter_dialogs():
            print(dialog.id, "\t", dialog.name)

    if args.list_messages:
        async for message in list_messages(args.list_messages):
            print(message.date, message.raw_text)


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
