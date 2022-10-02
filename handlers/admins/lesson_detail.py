from ..decorators import error_handler_decorator, is_admin_decorator
from functions.lessons import generate_lesson_message_and_buttons
from messages.globals.lessons import LESSON_NOT_FOUND
from telethon import events


@events.register(
    events.NewMessage(pattern="/lesson_detail_(\d+)", incoming=True)
)
@error_handler_decorator
@is_admin_decorator
async def lesson_detail_handler(event, database, user, is_programmer):
    lesson_id = int(event.pattern_match.group(1))

    lesson = database.get_lesson(id=lesson_id)

    if not lesson:
        await event.respond(LESSON_NOT_FOUND)
        return

    message, buttons = generate_lesson_message_and_buttons(lesson)

    await event.respond(message, buttons=buttons)
