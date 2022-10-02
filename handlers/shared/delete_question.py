from ..decorators import (
    conversation_protector_decorator, error_handler_decorator,
    is_user_decorator
)
from ..permissions import has_admins_permission
from database import QuestionStatus
from functions.globals import (
    get_user_confirm, send_message_to_user_even_is_blocked
)
from functions.questions import format_question_lesson_name
from helpers import remove_file
from messages.globals.questions import QUESTION_NOT_FOUND
from messages.shared.delete_question import *
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern=f"/delete_question_(\d+)")
)
@conversation_protector_decorator
@error_handler_decorator
@is_user_decorator
async def delete_question_handler(event, database, user):
    question_id = int(event.pattern_match.group(1))

    is_admin = has_admins_permission(user)

    if is_admin:
        question = database.get_question(id=question_id)

    else:
        question = database.get_question(id=question_id, user=user)

    if not question:
        await event.delete()
        await event.respond(QUESTION_NOT_FOUND)
        return

    await event.answer()

    user_confirm = await get_user_confirm(
        event.client, event.chat_id, DELETE_QUESTION_CONFIRM,
        DELETE_QUESTION_YES_BUTTON, DELETE_QUESTION_NO_BUTTON,
        DELETE_QUESTION_CANCELED
    )

    if user_confirm is None:
        return

    is_user_question = (question.user_id == user.id)

    question.status = QuestionStatus.CANCELED if (
        is_user_question
    ) else QuestionStatus.REMOVED

    for attachment in question.attachments:
        remove_file(attachment.path)

        database.delete(attachment)

    database.commit()

    await event.delete()

    if not is_user_question:
        await send_message_to_user_even_is_blocked(
            event.client,
            question.user.chat_id,
            YOUR_QUESTION_DELETED.format(
                question.title,
                format_question_lesson_name(question),
            )
        )

    await event.respond(
        DELETE_QUESTION_SUCCESSFUL, buttons=Button.clear()
    )
