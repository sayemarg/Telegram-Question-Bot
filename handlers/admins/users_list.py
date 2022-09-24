from ..constants import USERS_PAGINATION_LENGTH
from ..decorators import handle_error_decorator, is_admin_decorator
from functions.globals import create_list_message, generate_pagination_buttons
from functions.users import format_user_title, format_user_phone
from messages.admins.users_list import *
from messages.navigation import USERS_LIST_KEY
from messages.pagination import PAGE_DOES_NOT_EXISTS
from telethon import events


@events.register(
    events.CallbackQuery(pattern=f"^/users_list_(\d+)$")
)
@events.register(
    events.NewMessage(pattern=f"^{USERS_LIST_KEY}$", incoming=True)
)
@handle_error_decorator
@is_admin_decorator
async def users_list_handler(event, database, user, is_programmer):
    users_count = database.get_users_count()

    if not users_count:
        await event.respond(EMPTY_USERS_LIST)
        return

    is_callback_query = isinstance(event, events.CallbackQuery.Event)

    page_number = int(event.pattern_match.group(1)) if is_callback_query else 1

    start = (page_number - 1) * USERS_PAGINATION_LENGTH
    end = page_number * USERS_PAGINATION_LENGTH

    users_list = database.get_users_in_range(start, end)

    if not users_list:
        await event.edit(PAGE_DOES_NOT_EXISTS)
        return

    def format_user_function(counter, target_user): return (
        counter,
        format_user_title(target_user),
        target_user.full_name,
        format_user_phone(target_user, is_programmer),
    )

    list_message = create_list_message(
        users_list, users_count, start, USER_TEXT, format_user_function
    )

    buttons = generate_pagination_buttons(
        "/users_list_", USERS_PAGINATION_LENGTH, page_number, users_count
    )

    answer_function = event.edit if is_callback_query else event.respond

    await answer_function(list_message, buttons=buttons)
