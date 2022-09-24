from messages.admins.user_detail import (
    ADMIN_USER_HINT, NORMAL_USER_HINT, DIACTIVATED_USER_HINT,
    DIACTIVE_USER_BUTTON, ACTIVE_USER_BUTTON, DOWNGRADE_TO_USER_BUTTON,
    UPGRADE_TO_ADMIN_BUTTON, USER_DETAIL_TEXT
)
from messages.admins.users_list import (
    ADMIN_USER_TITLE, NORMAL_USER_TITLE, DIACTIVATED_USER_TITLE
)
from messages.globals.users import PHONE_HIDER_CHARACTER
from telethon import Button


def format_user_title(user):
    if not user.active:
        text = DIACTIVATED_USER_TITLE

    elif user.is_admin:
        text = ADMIN_USER_TITLE

    else:
        text = NORMAL_USER_TITLE

    return text.format(user.id)


def format_user_hint(user):
    if not user.active:
        text = DIACTIVATED_USER_HINT

    elif user.is_admin:
        text = ADMIN_USER_HINT

    else:
        text = NORMAL_USER_HINT

    return text.format(user.id)


def format_user_phone(user, is_programmer):
    if is_programmer:
        return user.phone_number

    phone_number = user.phone_number

    phone_length = len(phone_number)

    separation_size = phone_length // 3

    return (
        phone_number[:separation_size] +
        PHONE_HIDER_CHARACTER * (phone_length - 2 * separation_size) +
        phone_number[-separation_size:]
    )


def generate_user_message_and_buttons(user, is_programmer):
    buttons = []

    if (not user.is_admin) or (is_programmer):
        if user.active:
            buttons.append(
                Button.inline(
                    DIACTIVE_USER_BUTTON, f"/deactivate_user_{user.id}"
                ),
            )

        else:
            buttons.append(
                Button.inline(
                    ACTIVE_USER_BUTTON, f"/activate_user_{user.id}"
                ),
            )

    if is_programmer:
        if user.is_admin:
            buttons.append(
                Button.inline(
                    DOWNGRADE_TO_USER_BUTTON, f"/downgrade_admin_{user.id}"
                ),
            )

        else:
            buttons.append(
                Button.inline(
                    UPGRADE_TO_ADMIN_BUTTON, f"/upgrade_user_{user.id}"
                ),
            )

    return USER_DETAIL_TEXT.format(
        format_user_hint(user),
        user.chat_id,
        user.full_name,
        format_user_phone(user, is_programmer),
        user.created_at,
    ), (buttons or None)


async def update_user_message(event, target_user, is_programmer=True):
    message, buttons = generate_user_message_and_buttons(
        target_user, is_programmer
    )

    await event.edit(message, buttons=buttons)
