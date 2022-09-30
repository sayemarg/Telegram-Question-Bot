from ..constants import DOWNGRADE_REASON_MAX_LENGTH
from ..decorators import handle_error_decorator, is_programmer_decorator
from functions.globals import get_reason_from_user
from functions.users import update_user_message
from messages.admins.downgrade_admin import *
from messages.globals.users import USER_NOT_FOUND
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern="^/downgrade_admin_(\d+)$")
)
@handle_error_decorator()
@is_programmer_decorator
async def downgrade_admin_handler(event, database, user):
    user_id = int(event.pattern_match.group(1))

    target_user = database.get_user(id=user_id)

    if not target_user:
        await event.delete()
        await event.respond(USER_NOT_FOUND)
        return

    if not target_user.is_admin:
        await update_user_message(event, target_user)
        await event.respond(USER_IS_NOT_ADMIN)
        return

    await event.answer()

    provided_reason = await get_reason_from_user(
        event.client, event.chat_id, SEND_DOWNGRADE_REASON,
        DOWNGRADE_REASON_MAX_LENGTH, DOWNGRADE_ADMIN_CANCELED,
        DOWNGRADE_NOT_EMPTY_REASON, DOWNGRADE_NO_REASON_PROVIDED
    )

    if provided_reason is None:
        return

    database.delete(target_user.admin)

    database.commit()

    await event.client.send_message(
        target_user.chat_id,
        DOWNGRADED_TO_USER_MESSAGE.format(provided_reason),
        buttons=Button.clear()
    )

    await update_user_message(event, target_user)

    await event.respond(
        DOWNGRADE_ADMIN_SUCCESSFULLY,
        buttons=Button.clear()
    )
