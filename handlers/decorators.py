from .constants import CONVERSATION_TIMEOUT
from .permissions import has_user_permission, is_user_programmer
from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from database import DatabaseManager
from helpers import PROGRAMMER_CHAT_ID, remove_file
from messages.decorators import *
from telethon import Button
from traceback import format_exc


async def send_report_to_programmer(bot, message, chat_id):
    path = f"./temp/report_{chat_id}.txt"

    with open(path, "w") as report_file:
        report_file.write(message)

    await bot.send_file(PROGRAMMER_CHAT_ID, path)

    remove_file(path)


def handle_error_decorator(callback):
    async def inner(event):
        try:
            database = DatabaseManager()

            user = database.get_user(chat_id=event.chat_id)

            await callback(event, database, user)

        except AsyncioTimeoutError:
            timeout_minutes = CONVERSATION_TIMEOUT // 60

            await event.respond(
                CONVERSATION_TIMEOUT_EXCEEDED.format(
                    timeout_minutes
                )
            )

        except:
            await event.respond(BOT_ERROR_OCCURED)

            command = event.pattern_match.string

            if isinstance(command, bytes):
                command = command.decode()

            await send_report_to_programmer(
                event.client,
                ADMIN_ERROR_REPORT.format(
                    command,
                    format_exc(),
                ),
                event.chat_id
            )

        finally:
            database.close()

    return inner


def is_user_decorator(callback):
    async def inner(event, database, user):
        if not has_user_permission(user):
            await event.respond(
                YOU_ARE_NOT_USER, buttons=Button.clear()
            )
            return

        await callback(event, database, user)

    return inner


def is_admin_decorator(callback):
    async def inner(event, database, user):
        if not has_user_permission(user):
            await event.respond(
                YOU_ARE_NOT_USER, buttons=Button.clear()
            )
            return

        is_programmer = is_user_programmer(user)

        if (
            (not is_programmer) and
            (not user.is_admin)
        ):
            await event.respond(
                YOU_ARE_NOT_ADMIN, buttons=Button.clear()
            )
            return

        await callback(event, database, user, is_programmer)

    return inner


def is_programmer_decorator(callback):
    async def inner(event, database, user):
        if not has_user_permission(user):
            await event.respond(
                YOU_ARE_NOT_USER, buttons=Button.clear()
            )
            return

        if not is_user_programmer(user):
            await event.respond(
                YOU_ARE_NOT_PROGRAMMER, buttons=Button.clear()
            )
            return

        await callback(event, database, user)

    return inner
