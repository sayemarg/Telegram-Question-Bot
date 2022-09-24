from ..decorators import handle_error_decorator, is_admin_decorator
from functions.users import generate_user_message_and_buttons
from messages.admins.user_detail import IS_SELF_USER
from messages.globals.users import USER_NOT_FOUND
from telethon import events


@events.register(
    events.NewMessage(pattern="/user_detail_(\d+)", incoming=True)
)
@handle_error_decorator
@is_admin_decorator
async def user_detail_handler(event, database, user, is_programmer):
    user_id = int(event.pattern_match.group(1))

    if (not is_programmer) and (user_id == user.id):
        await event.respond(IS_SELF_USER)
        return

    target_user = database.get_user(id=user_id)

    if not target_user:
        await event.respond(USER_NOT_FOUND)
        return

    user_message, user_buttons = generate_user_message_and_buttons(
        target_user, is_programmer
    )

    await event.respond(
        user_message,
        buttons=user_buttons
    )
