from ..constants import CONVERSATION_TIMEOUT, LESSON_TITLE_MAX_LENGTH
from ..decorators import handle_error_decorator, is_admin_decorator
from functions.lessons import generate_lesson_message_and_buttons
from messages.admins.add_lesson import *
from messages.navigation import ADD_LESSON_KEY
from telethon import events


@events.register(
    events.NewMessage(pattern=f"^{ADD_LESSON_KEY}$", incoming=True)
)
@handle_error_decorator
@is_admin_decorator
async def add_lesson_handler(event, database, user, is_programmer):
    async with event.client.conversation(
        event.chat_id, timeout=CONVERSATION_TIMEOUT
    ) as conversation:
        await conversation.send_message(SEND_LESSON_TITLE)

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(ADD_LESSON_CANCELED)
                return

            if not response.raw_text:
                await conversation.send_message(NO_EMPTY_TITLE)
                continue

            if LESSON_TITLE_MAX_LENGTH < len(response.raw_text):
                await conversation.send_message(
                    TITLE_MAX_LENGTH.format(LESSON_TITLE_MAX_LENGTH)
                )
                continue

            break

    lesson = database.get_lesson(title=response.raw_text)

    if lesson:
        await event.respond(
            LESSON_TITLE_EXISTS.format(lesson.id)
        )
        return

    lesson = database.create_lesson(
        title=response.raw_text, admin=user.admin
    )

    database.commit()

    message, buttons = generate_lesson_message_and_buttons(lesson)

    await event.respond(message, buttons=buttons)
