from ..constants import QUESTIONS_PAGINATION_LENGTH
from ..decorators import handle_error_decorator, is_admin_decorator
from functions.globals import create_list_message, generate_pagination_buttons
from functions.questions import format_question_preview_function
from messages.admins.lesson_questions import *
from messages.globals.lessons import LESSON_NOT_FOUND
from messages.globals.questions import QUESTION_TEXT
from messages.pagination import PAGE_DOES_NOT_EXISTS
from telethon import events


@events.register(
    events.CallbackQuery(pattern=f"/lesson_questions_(\d+)_(\d+)")
)
@handle_error_decorator
@is_admin_decorator
async def lesson_questions_handler(event, database, user, is_programmer):
    lesson_id = int(event.pattern_match.group(1))

    lesson = database.get_lesson(id=lesson_id)

    if not lesson:
        await event.delete()
        await event.respond(LESSON_NOT_FOUND)
        return

    questions_count = database.get_questions_count(lesson=lesson)

    if not questions_count:
        await event.respond(EMPTY_QUESTIONS_LIST)
        return

    page_number = int(event.pattern_match.group(2))

    start = (page_number - 1) * QUESTIONS_PAGINATION_LENGTH
    end = page_number * QUESTIONS_PAGINATION_LENGTH

    questions_list = database.get_questions_in_range(start, end, lesson=lesson)

    if not questions_list:
        await event.edit(PAGE_DOES_NOT_EXISTS)
        return

    list_message = create_list_message(
        questions_list, questions_count, start, QUESTION_TEXT,
        format_question_preview_function
    )

    buttons = generate_pagination_buttons(
        f"/lesson_questions_{lesson_id}_", QUESTIONS_PAGINATION_LENGTH,
        page_number, questions_count
    )

    await event.edit(list_message, buttons=buttons)
