from ..constants import FULL_NAME_MAX_LENGTH
from ..decorators import handle_error_decorator
from helpers import create_path_if_not_exists
from messages.shared.start import *
from telethon import events, Button


@events.register(
    events.NewMessage(pattern="^/start$", incoming=True)
)
@handle_error_decorator
async def start_handler(event, database, user):
    chat = await event.get_chat()

    await event.respond(
        WELCOME_MESSAGE.format(chat.first_name)
    )

    if user:
        if user.active:
            await event.respond(HAS_ACCESS)
            return

        else:
            await event.respond(ACCOUNT_DEACTIVATED)
            return

    async with event.client.conversation(chat.id, timeout=None) as conversation:
        await conversation.send_message(SEND_FULL_NAME)

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(CANCEL_ACCESS_PROCESS)
                conversation.cancel()
                return

            full_name = response.raw_text.split()

            if len(full_name) < 2:
                await conversation.send_message(FULL_NAME_WORDS_LIMIT)
                continue

            full_name = " ".join(full_name)

            if FULL_NAME_MAX_LENGTH < len(full_name):
                await conversation.send_message(
                    FULL_NAME_LENGTH_LIMIT.format(FULL_NAME_MAX_LENGTH)
                )
                continue

            break

        await conversation.send_message(
            SHARE_YOUR_PHONE,
            buttons=Button.request_phone(
                SHARE_PHONE_BUTTON, resize=True, single_use=True
            )
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(
                    CANCEL_ACCESS_PROCESS, buttons=Button.clear()
                )
                conversation.cancel()
                return

            contact = response.contact

            if not contact:
                await conversation.send_message(SEND_PHONE_TO_ACCESS)
                continue

            if contact.user_id != chat.id:
                await conversation.send_message(SEND_YOUR_PHONE_TO_ACCESS)
                continue

            break

    user = database.create_user(
        chat_id=chat.id, full_name=full_name, phone=contact.phone_number
    )

    database.commit()

    create_path_if_not_exists(f"./files/{chat.id}/")

    await event.respond(ACCESS_GRANTED)
