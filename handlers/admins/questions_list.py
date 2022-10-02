from ..constants import QUESTIONS_PAGINATION_LENGTH
from ..decorators import error_handler_decorator, is_admin_decorator
from functions.globals import create_list_message, generate_pagination_buttons
from functions.questions import format_question_preview_function
from messages.globals.questions import QUESTION_TEXT
from messages.navigation import ALL_QUESTIONS_LIST_KEY
from messages.pagination import PAGE_DOES_NOT_EXISTS
from messages.admins.questions_list import *
from telethon import events


@events.register(
    events.CallbackQuery(pattern=f"/all_questions_(\d+)")
)
@events.register(
    events.NewMessage(pattern=f"^{ALL_QUESTIONS_LIST_KEY}$", incoming=True)
)
@error_handler_decorator
@is_admin_decorator
async def all_questions_list_handler(event, database, user, is_programmer):
    questions_count = database.get_questions_count()

    if not questions_count:
        await event.respond(EMPTY_QUESTIONS_LIST)
        return

    is_callback_query = isinstance(event, events.CallbackQuery.Event)

    page_number = int(event.pattern_match.group(1)) if is_callback_query else 1

    start = (page_number - 1) * QUESTIONS_PAGINATION_LENGTH
    end = page_number * QUESTIONS_PAGINATION_LENGTH

    questions_list = database.get_questions_in_range(start, end)

    if not questions_list:
        await event.edit(PAGE_DOES_NOT_EXISTS)
        return

    list_message = create_list_message(
        questions_list, questions_count, start, QUESTION_TEXT,
        format_question_preview_function
    )

    buttons = generate_pagination_buttons(
        "/all_questions_", QUESTIONS_PAGINATION_LENGTH, page_number, questions_count
    )

    answer_function = event.edit if is_callback_query else event.respond

    await answer_function(list_message, buttons=buttons)
