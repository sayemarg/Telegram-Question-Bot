from ..decorators import (
    conversation_protector_decorator, error_handler_decorator,
    is_admin_decorator
)
from functions.globals import get_user_confirm
from messages.admins.delete_lesson import *
from messages.globals.lessons import LESSON_NOT_FOUND
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern="^/delete_lesson_(\d+)$")
)
@conversation_protector_decorator
@error_handler_decorator
@is_admin_decorator
async def delete_lesson_handler(event, database, user, is_programmer):
    lesson_id = int(event.pattern_match.group(1))

    lesson = database.get_lesson(id=lesson_id)

    if not lesson:
        await event.delete()
        await event.respond(LESSON_NOT_FOUND)
        return

    await event.answer()

    user_confirm = await get_user_confirm(
        event.client, event.chat_id, DELETE_LESSON_CONFIRM,
        DELETE_LESSON_YES_BUTTON, DELETE_LESSON_NO_BUTTON, DELETE_LESSON_CANCELED
    )

    if not user_confirm:
        return

    database.delete(lesson)

    database.commit()

    await event.delete()

    await event.respond(DELETE_LESSON_SUCCESSFUL, buttons=Button.clear())
