from ..constants import DELETE_ATTACHMENT_REASON_MAX_LENGTH
from ..decorators import (
    conversation_protector_decorator, error_handler_decorator,
    is_user_decorator
)
from ..permissions import has_admins_permission
from functions.globals import (
    get_user_confirm, get_reason_from_user, send_message_to_user_even_is_blocked
)
from helpers import remove_file
from messages.shared.delete_attachment import *
from telethon import events, Button


async def delete_attachment_by_admin(event, database, attachment):
    privided_reason = await get_reason_from_user(
        event.client, event.chat_id, SEND_DELETE_ATTACHMENT_REASON,
        DELETE_ATTACHMENT_REASON_MAX_LENGTH, DELETE_ATTACHMENT_CANCELED,
        NO_EMPTY_REASON, REASON_SKIPPED
    )

    if privided_reason is None:
        return

    remove_file(attachment.path)

    database.delete(attachment)

    database.commit()

    await event.delete()

    await send_message_to_user_even_is_blocked(
        event.client,
        attachment.question.user.chat_id,
        YOUR_ATTACHMENT_DELETED.format(
            attachment.question.title,
            privided_reason
        )
    )

    await event.respond(
        DELETE_ATTACHMENT_SUCCESSFUL,
        buttons=Button.clear()
    )


async def delete_attachment_by_user(event, database, attachment):
    user_confirm = await get_user_confirm(
        event.client, event.chat_id, DELETE_ATTACHMENT_CONFIRM,
        DELETE_ATTACHMENT_YES_BUTTON, DELETE_ATTACHMENT_NO_BUTTON,
        DELETE_ATTACHMENT_CANCELED
    )

    if user_confirm is None:
        return

    remove_file(attachment.path)

    database.delete(attachment)

    database.commit()

    await event.delete()

    await event.respond(
        DELETE_ATTACHMENT_SUCCESSFUL,
        buttons=Button.clear()
    )


@events.register(
    events.CallbackQuery(pattern=f"/delete_attachment_(\d+)")
)
@conversation_protector_decorator
@error_handler_decorator
@is_user_decorator
async def delete_attachment_handler(event, database, user):
    attachment_id = int(event.pattern_match.group(1))

    attachment = database.get_attachment(id=attachment_id)

    if not attachment:
        await event.delete()
        await event.respond(ATTACHMENT_NOT_FOUND)
        return

    is_admin = has_admins_permission(user)

    is_user_attachment = (attachment.question.user_id == user.id)

    if (
        (not is_user_attachment) and
        (not is_admin)
    ):
        await event.respond(CAN_NOT_DELETE_OTHERS_ATTACHMENT)
        return

    await event.answer()

    if is_user_attachment:
        await delete_attachment_by_user(event, database, attachment)

    else:
        await delete_attachment_by_admin(event, database, attachment)
