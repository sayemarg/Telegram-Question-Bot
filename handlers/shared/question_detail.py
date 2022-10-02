from ..decorators import error_handler_decorator, is_user_decorator
from ..permissions import has_admins_permission
from functions.questions import generate_question_message_and_buttons
from messages.globals.questions import QUESTION_NOT_FOUND
from telethon import events


@events.register(
    events.NewMessage(pattern="/question_detail_(\d+)", incoming=True)
)
@error_handler_decorator
@is_user_decorator
async def question_detail_handler(event, database, user):
    question_id = int(event.pattern_match.group(1))

    is_admin = has_admins_permission(user)

    if is_admin:
        question = database.get_question(id=question_id)

    else:
        question = database.get_question(id=question_id, user=user)

    if not question:
        await event.respond(QUESTION_NOT_FOUND)
        return

    message, buttons = generate_question_message_and_buttons(
        question, user, is_admin
    )

    await event.respond(message, buttons=buttons)
