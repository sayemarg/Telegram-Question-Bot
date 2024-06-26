from ..decorators import error_handler_decorator, is_admin_decorator
from functions.globals import send_message_to_user_even_is_blocked
from functions.users import update_user_message
from messages.admins.activate_user import *
from messages.globals.users import (
    CAN_NOT_MODIFY_SELF, USER_NOT_FOUND, CAN_NOT_MODIFY_ADMINS
)
from telethon import events


@events.register(
    events.CallbackQuery(pattern="^/activate_user_(\d+)$")
)
@error_handler_decorator
@is_admin_decorator
async def activate_user_handler(event, database, user, is_programmer):
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

    if target_user.active:
        await update_user_message(event, target_user, is_programmer)
        await event.respond(USER_IS_ACTIVE)
        return

    target_user.active = True

    database.commit()

    await send_message_to_user_even_is_blocked(
        event.client,
        target_user.chat_id,
        ACCOUNT_ACTIVATED_MESSAGE
    )

    await update_user_message(event, target_user, is_programmer)

    await event.respond(USER_ACTIVATED)
