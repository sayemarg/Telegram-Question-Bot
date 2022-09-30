from ..decorators import handle_error_decorator, is_programmer_decorator
from functions.globals import get_user_confirm
from functions.users import update_user_message
from messages.admins.upgrade_user import *
from messages.globals.users import USER_NOT_FOUND
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern="^/upgrade_user_(\d+)$")
)
@handle_error_decorator()
@is_programmer_decorator
async def upgrade_user_handler(event, database, user):
    user_id = int(event.pattern_match.group(1))

    target_user = database.get_user(id=user_id)

    if not target_user:
        await event.delete()
        await event.respond(USER_NOT_FOUND)
        return

    if target_user.is_admin:
        await update_user_message(event, target_user)
        await event.respond(USER_IS_ADMIN)
        return

    await event.answer()

    user_confirm = await get_user_confirm(
        event.client, event.chat_id, UPGRADE_USER_CONFIRM,
        UPGRADE_USER_YES_BUTTON, UPGRADE_USER_NO_BUTTON, UPGRADE_USER_CANCELED
    )

    if not user_confirm:
        return

    if not target_user.active:
        target_user.active = True

    database.create_admin(user_id=user_id)

    database.commit()

    await event.client.send_message(
        target_user.chat_id,
        UPGRADED_TO_ADMIN_MESSAGE
    )

    await update_user_message(event, target_user)

    await event.respond(
        UPGRADE_USER_SUCCESSFUL,
        buttons=Button.clear()
    )
