from database import create_database_metadata
from handlers import BOT_EVENT_HANDLERS
from helpers import API_ID, API_HASH, BOT_TOKEN, create_path_if_not_exists
from telethon.sync import TelegramClient, connection


def create_required_dirs():
    create_path_if_not_exists("temp")
    create_path_if_not_exists("files")


def main():
    create_required_dirs()

    create_database_metadata()

    bot = TelegramClient(
        "Bot", API_ID, API_HASH,
        connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
        proxy=("mjd.sabouni.co", 443, "dd00000000000000000000000000000000")
    )
    bot.start(bot_token=BOT_TOKEN)

    for event_handler in BOT_EVENT_HANDLERS:
        bot.add_event_handler(event_handler)

    bot.run_until_disconnected()


if __name__ == "__main__":
    main()
