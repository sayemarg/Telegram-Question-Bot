from ..constants import PICTURE_MAX_SIZE, VIDEO_MAX_SIZE, SOUND_MAX_SIZE
from ..decorators import handle_error_decorator, is_user_decorator
from messages.globals.questions import QUESTION_NOT_FOUND
from messages.users.attach_file import *
from telethon import events


@events.register(
    events.CallbackQuery(pattern=f"/attach_file_(\d+)")
)
@handle_error_decorator
@is_user_decorator
async def attach_file_handler(event, database, user):
    question_id = int(event.pattern_match.group(1))

    question = database.get_question(id=question_id, user=user)

    if not question:
        await event.respond(QUESTION_NOT_FOUND)
        return

    await event.answer()

    async with event.client.conversation(event.chat_id) as conversation:
        await conversation.send_message(
            SEND_FILE.format(PICTURE_MAX_SIZE, VIDEO_MAX_SIZE, SOUND_MAX_SIZE)
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(ATTACH_FILE_CANCELED)
                return

            # TODO: Check file type and constraints

            break

    file_path = await response.download_media(f"./files/{event.chat_id}")

    database.create_attachment(
        path=file_path, question=question
    )

    database.commit()

    await event.respond(ATTACH_FILE_SUCCESSFUL)
