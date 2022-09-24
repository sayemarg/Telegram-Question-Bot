from ..decorators import handle_error_decorator, is_user_decorator
from ..permissions import has_admins_permission
from messages.shared.main_menu import *
from messages.navigation import (
    NEW_QUESTION_KEY, MY_QUESTIONS_LIST_KEY, ADD_LESSON_KEY,
    LESSONS_LIST_KEY, ALL_QUESTIONS_LIST_KEY, USERS_LIST_KEY
)
from telethon import events, Button


@events.register(
    events.NewMessage(pattern="^/main_menu$", incoming=True)
)
@handle_error_decorator
@is_user_decorator
async def main_menu_handler(event, database, user):
    buttons = [
        [
            Button.text(NEW_QUESTION_KEY, resize=True, single_use=True),
            Button.text(MY_QUESTIONS_LIST_KEY, resize=True, single_use=True),
        ],
    ]

    if has_admins_permission(user):
        buttons += [
            [
                Button.text(ADD_LESSON_KEY, resize=True, single_use=True),
                Button.text(LESSONS_LIST_KEY, resize=True, single_use=True),
            ],
            [
                Button.text(
                    ALL_QUESTIONS_LIST_KEY, resize=True, single_use=True
                ),
                Button.text(USERS_LIST_KEY, resize=True, single_use=True),
            ]
        ]

    await event.respond(MAIN_MENU_TEXT, buttons=buttons)
