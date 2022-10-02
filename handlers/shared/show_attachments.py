from ..decorators import error_handler_decorator, is_user_decorator
from ..permissions import has_admins_permission
from helpers import FILES_CHANNEL_ID
from messages.globals.questions import QUESTION_NOT_FOUND
from messages.shared.show_attachments import *
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern=f"/show_attachments_(\d+)")
)
@error_handler_decorator
@is_user_decorator
async def show_attachments_handler(event, database, user):
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

    attachments = database.get_attachments_list(question=question)

    if not attachments:
        await event.respond(EMPTY_ATTACHMENTS)
        return

    for attachment in attachments:
        message = await event.client.get_messages(
            FILES_CHANNEL_ID,
            ids=attachment.message_id
        )

        button = Button.inline(
            DELETE_ATTACHMENT_BUTTON, f"/delete_attachment_{attachment.id}"
        )

        if not message:
            await event.reply(ATTACHMENT_DOSE_NOT_EXISTS, buttons=button)
            continue

        await event.reply(message, buttons=button)
