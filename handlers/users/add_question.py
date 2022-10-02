from ..constants import (
    CONVERSATION_TIMEOUT, QUESTION_TITLE_MAX_LENGTH, QUESTION_TEXT_MAX_LENGTH
)
from ..decorators import (
    conversation_protector_decorator, error_handler_decorator,
    is_user_decorator
)
from ..permissions import has_admins_permission
from functions.globals import send_message_to_user_even_is_blocked
from functions.questions import generate_question_message_and_buttons
from messages.navigation import NEW_QUESTION_KEY
from messages.users.add_question import *
from re import match
from telethon import events, Button


@events.register(
    events.NewMessage(pattern=f"^{NEW_QUESTION_KEY}$", incoming=True)
)
@conversation_protector_decorator
@error_handler_decorator
@is_user_decorator
async def add_question_handler(event, databse, user):
    lessons = databse.get_lessons_list()

    if not lessons:
        await event.respond(EMPLTY_LESSONS_LIST)
        return

    lesson_buttons = [
        [Button.inline(lesson.title, f"{SELECT_LESSON_PREFIX}_{lesson.id}")]
        for lesson in lessons
    ]

    lesson_buttons.append([
        Button.inline(CANCEL_SELECT, f"{SELECT_LESSON_PREFIX}_cancel")
    ])

    select_event_match_pattern = f"{SELECT_LESSON_PREFIX}_(cancel|[1-9]\d*)"

    async with event.client.conversation(
        event.chat_id, timeout=CONVERSATION_TIMEOUT
    ) as conversation:
        select_message = await conversation.send_message(
            SELECT_LESSON, buttons=lesson_buttons
        )

        user_select_event = await conversation.wait_event(
            events.CallbackQuery(
                pattern=select_event_match_pattern,
                func=lambda select_event: (
                    (select_event.query.user_id == event.chat_id) and
                    (select_event.query.msg_id == select_message.id)
                ),
            )
        )

        await user_select_event.delete()

        selected_lesson = match(
            select_event_match_pattern, user_select_event.data.decode()
        ).group(1)

        if selected_lesson == "cancel":
            await conversation.send_message(ADD_QUESTION_CANCELED)
            return

        lesson_id = int(selected_lesson)

        await conversation.send_message(
            SEND_QUESTION_TITLE.format(QUESTION_TITLE_MAX_LENGTH)
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(ADD_QUESTION_CANCELED)
                return

            if not response.raw_text:
                await conversation.send_message(NO_EMPTY_TITLE)
                continue

            if QUESTION_TITLE_MAX_LENGTH < len(response.raw_text):
                await conversation.send_message(
                    TITLE_LENGTH_LIMIT.format(QUESTION_TITLE_MAX_LENGTH)
                )
                continue

            title = response.raw_text

            break

        await conversation.send_message(
            SEND_QUESTION_TEXT.format(QUESTION_TEXT_MAX_LENGTH)
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(ADD_QUESTION_CANCELED)
                return

            if not response.raw_text:
                await conversation.send_message(NO_EMPTY_TEXT)
                continue

            if QUESTION_TEXT_MAX_LENGTH < len(response.raw_text):
                await conversation.send_message(
                    TEXT_LENGTH_LIMIT.format(QUESTION_TEXT_MAX_LENGTH)
                )
                continue

            text = response.raw_text

            break

    lesson = databse.get_lesson(id=lesson_id)

    question = databse.create_question(
        title=title, text=text, lesson=lesson, user=user
    )

    databse.commit()

    message, buttons = generate_question_message_and_buttons(
        question, user, has_admins_permission(user)
    )

    await event.respond(message, buttons=buttons)

    admins_list = databse.get_admins_list()

    admins_message = NEW_QUESTION_SUBMITTED.format(question.id)

    for admin in admins_list:
        await send_message_to_user_even_is_blocked(
            event.client,
            admin.user.chat_id,
            admins_message
        )
