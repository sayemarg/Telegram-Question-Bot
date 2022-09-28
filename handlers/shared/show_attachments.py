from ..decorators import handle_error_decorator, is_user_decorator
from ..permissions import has_admins_permission
from helpers import path_exists
from messages.globals.questions import QUESTION_NOT_FOUND
from messages.shared.show_attachments import *
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern=f"/show_attachments_(\d+)")
)
@handle_error_decorator
@is_user_decorator
async def show_attachments_handler(event, database, user):
    question_id = int(event.pattern_match.group(1))

    is_admin = has_admins_permission(user)

    if is_admin:
        question = database.get_question(id=question_id)

    else:
        question = database.get_question(id=question_id, user=user)

    if not question:
        await event.respond(QUESTION_NOT_FOUND)
        return

    attachments = database.get_attachments_list(question=question)

    if not attachments:
        await event.respond(EMPTY_ATTACHMENTS)
        return

    for attachment in attachments:
        file_path = attachment.path

        if not path_exists(file_path):
            continue

        await event.respond(
            file=file_path,
            buttons=Button.inline(
                DELETE_ATTACHMENT_BUTTON, f"/delete_attachment_{attachment.id}"
            )
        )
