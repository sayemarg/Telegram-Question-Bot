from dotenv import load_dotenv
from os import getenv, path, mkdir, remove

load_dotenv("./.env")

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")

PROGRAMMER_CHAT_ID = int(getenv("PROGRAMMER_CHAT_ID"))


def create_path_if_not_exists(file_name):
    if path.exists(file_name):
        return

    mkdir(file_name)


def remove_file(file_path):
    if not path.exists(file_path):
        return

    remove(file_path)


def path_exists(file_path):
    return path.exists(file_path)
