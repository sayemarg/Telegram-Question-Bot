from ..constants import DELETE_ATTACHMENT_REASON_MAX_LENGTH
from ..decorators import (
    conversation_protector_decorator, error_handler_decorator,
    is_user_decorator
)
from ..permissions import has_admins_permission
from functions.globals import (
    get_user_confirm, get_reason_from_user, send_message_to_user_even_is_blocked
)
from helpers import FILES_CHANNEL_ID
from messages.shared.delete_attachment import *
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern=f"/delete_attachment_(\d+)")
)
@conversation_protector_decorator
@error_handler_decorator
@is_user_decorator
async def delete_attachment_handler(event, database, user):
    attachment_id = int(event.pattern_match.group(1))

    is_admin = has_admins_permission(user)

    if is_admin:
        attachment = database.get_attachment(id=attachment_id)

    else:
        attachment = database.get_attachment(id=attachment_id, user=user)

    if not attachment:
        await event.delete()
        await event.respond(ATTACHMENT_NOT_FOUND)
        return

    is_user_attachment = (attachment.user_id == user.id)

    await event.answer()

    if is_user_attachment:
        user_response = await get_user_confirm(
            event.client, event.chat_id, DELETE_ATTACHMENT_CONFIRM,
            DELETE_ATTACHMENT_YES_BUTTON, DELETE_ATTACHMENT_NO_BUTTON,
            DELETE_ATTACHMENT_CANCELED
        )

    else:
        user_response = await get_reason_from_user(
            event.client, event.chat_id, SEND_DELETE_ATTACHMENT_REASON,
            DELETE_ATTACHMENT_REASON_MAX_LENGTH, DELETE_ATTACHMENT_CANCELED,
            NO_EMPTY_REASON, REASON_SKIPPED
        )

    if user_response is None:
        return

    database.delete(attachment)

    database.commit()

    await event.delete()

    await event.client.delete_messages(
        FILES_CHANNEL_ID,
        message_ids=attachment.message_id
    )

    if not is_user_attachment:
        await send_message_to_user_even_is_blocked(
            event.client,
            attachment.user.chat_id,
            YOUR_ATTACHMENT_DELETED.format(
                attachment.question.title,
                user_response
            )
        )

    await event.respond(
        DELETE_ATTACHMENT_SUCCESSFUL,
        buttons=Button.clear()
    )
