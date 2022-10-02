from ..constants import LESSONS_PAGINATION_LENGTH
from ..decorators import error_handler_decorator, is_admin_decorator
from functions.globals import create_list_message, generate_pagination_buttons
from functions.lessons import format_lesson_preview_function
from messages.admins.lessons_list import *
from messages.navigation import LESSONS_LIST_KEY
from messages.pagination import PAGE_DOES_NOT_EXISTS
from telethon import events


@events.register(
    events.CallbackQuery(pattern=f"^/lessons_list_(\d+)$")
)
@events.register(
    events.NewMessage(pattern=f"^{LESSONS_LIST_KEY}$", incoming=True)
)
@error_handler_decorator
@is_admin_decorator
async def lessons_list_handler(event, database, user, is_programmer):
    lessons_count = database.get_lessons_count()

    if not lessons_count:
        await event.respond(EMPTY_LESSONS_LIST)
        return

    is_callback_query = isinstance(event, events.CallbackQuery.Event)

    page_number = int(event.pattern_match.group(1)) if is_callback_query else 1

    start = (page_number - 1) * LESSONS_PAGINATION_LENGTH
    end = page_number * LESSONS_PAGINATION_LENGTH

    lessons_list = database.get_lessons_in_range(start, end)

    if not lessons_list:
        await event.edit(PAGE_DOES_NOT_EXISTS)
        return

    list_message = create_list_message(
        lessons_list, lessons_count, start, LESSON_TEXT, format_lesson_preview_function
    )

    buttons = generate_pagination_buttons(
        "/lessons_list_", LESSONS_PAGINATION_LENGTH, page_number, lessons_count
    )

    answer_function = event.edit if is_callback_query else event.respond

    await answer_function(list_message, buttons=buttons)
