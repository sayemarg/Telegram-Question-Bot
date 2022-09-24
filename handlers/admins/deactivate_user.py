from ..constants import ACCOUNT_DEACTIVATE_REASON_MAX_LENGTH
from ..decorators import handle_error_decorator, is_admin_decorator
from functions.globals import get_reason_from_user
from functions.users import update_user_message
from messages.admins.deactivate_user import *
from messages.globals.users import (
    CAN_NOT_MODIFY_SELF, USER_NOT_FOUND, CAN_NOT_MODIFY_ADMINS
)
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern="^/deactivate_user_(\d+)$")
)
@handle_error_decorator
@is_admin_decorator
async def deactivate_user_handler(event, database, user, is_programmer):
    user_id = int(event.pattern_match.group(1))

    if (not is_programmer) and (user_id == user.id):
        await event.respond(CAN_NOT_MODIFY_SELF)
        return

    target_user = database.get_user(id=user_id)

    if not target_user:
        await event.delete()
        await event.respond(USER_NOT_FOUND)
        return

    if (not is_programmer) and (target_user.is_admin):
        await update_user_message(event, target_user, is_programmer)
        await event.respond(CAN_NOT_MODIFY_ADMINS)
        return

    if not target_user.active:
        await update_user_message(event, target_user, is_programmer)
        await event.respond(USER_IS_DEACTIVE)
        return

    await event.answer()

    provided_reason = await get_reason_from_user(
        event.client, event.chat_id, SEND_DEACTIVATION_REASON,
        ACCOUNT_DEACTIVATE_REASON_MAX_LENGTH, DEACTIVE_USER_CANCELED,
        NOT_EMPTY_REASON, NO_REASON_PROVIDED
    )

    if provided_reason is None:
        return

    target_user.active = False

    if target_user.is_admin:
        database.delete(target_user.admin)

    database.commit()

    await event.client.send_message(
        target_user.chat_id,
        ACCOUNT_DEACTIVATED_MESSAGE.format(provided_reason),
        buttons=Button.clear()
    )

    await update_user_message(event, target_user, is_programmer)

    await event.respond(
        USER_DEACTIVATED,
        buttons=Button.clear()
    )
