from ..constants import (
    CONVERSATION_TIMEOUT, QUESTION_ATTACHMENT_MAX_NUMBER, PICTURE_MAX_SIZE,
    VIDEO_MAX_SIZE, SOUND_MAX_SIZE
)
from ..decorators import (
    conversation_protector_decorator, error_handler_decorator,
    is_user_decorator
)
from helpers import FILES_CHANNEL_ID
from messages.globals.questions import QUESTION_NOT_FOUND
from messages.users.attach_file import *
from telethon import events


@events.register(
    events.CallbackQuery(pattern=f"/attach_file_(\d+)")
)
@conversation_protector_decorator
@error_handler_decorator
@is_user_decorator
async def attach_file_handler(event, database, user):
    question_id = int(event.pattern_match.group(1))

    question = database.get_question(id=question_id, user=user)

    if not question:
        await event.delete()
        await event.respond(QUESTION_NOT_FOUND)
        return

    attachment_count = database.get_attachments_count(question=question)

    if QUESTION_ATTACHMENT_MAX_NUMBER <= attachment_count:
        await event.respond(
            MAX_ATTACHMENT_NUMBER.format(QUESTION_ATTACHMENT_MAX_NUMBER)
        )
        return

    await event.answer()

    async with event.client.conversation(
        event.chat_id, timeout=CONVERSATION_TIMEOUT
    ) as conversation:
        await conversation.send_message(SEND_FILE)

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(ATTACH_FILE_CANCELED)
                return

            if not response.media:
                await conversation.send_message(FILE_IS_REQUIRED)
                continue

            break

    message = await event.client.send_message(
        FILES_CHANNEL_ID,
        response
    )

    database.create_attachment(
        message_id=message.id, question=question, user=user
    )

    database.commit()

    await event.respond(ATTACH_FILE_SUCCESSFUL)
