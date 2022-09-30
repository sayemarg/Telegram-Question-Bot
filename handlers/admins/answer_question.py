from ..constants import ANSWER_QUESTION_MAX_NUMBER
from ..decorators import handle_error_decorator, is_admin_decorator
from database import QuestionStatus
from functions.questions import (
    format_question_lesson_name, update_question_message
)
from messages.admins.answer_question import *
from messages.globals.questions import QUESTION_NOT_FOUND
from telethon import events, Button


@events.register(
    events.CallbackQuery(pattern=f"/answer_question_(\d+)")
)
@handle_error_decorator
@is_admin_decorator
async def answer_question_handler(event, database, user, is_programmer):
    question_id = int(event.pattern_match.group(1))

    question = database.get_question(id=question_id)

    if not question:
        await event.delete()
        await event.respond(QUESTION_NOT_FOUND)
        return

    await event.answer()

    answer_messages = []

    async with event.client.conversation(
        event.chat_id, timeout=None
    ) as conversation:
        await conversation.send_message(
            SEND_YOUR_ANSWERS.format(ANSWER_QUESTION_MAX_NUMBER),
            buttons=Button.text(
                SEND_ANSWER_DONE, resize=True, single_use=True
            )
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(
                    ANSWER_QUESTION_CANCELED, buttons=Button.clear()
                )
                return

            if response.raw_text == SEND_ANSWER_DONE:
                break

            answer_messages.append(response)

            if ANSWER_QUESTION_MAX_NUMBER <= len(answer_messages):
                await conversation.send_message(ANSWER_NUMBERS_LIMIT)
                break

    user_chat_id = question.user.chat_id

    await event.client.send_message(
        user_chat_id,
        YOUR_QUESTION_ANSWERS.format(
            question.id,
            question.title,
            format_question_lesson_name(question)
        )
    )

    for message in answer_messages:
        await event.client.send_message(user_chat_id, message)

    if question.status == QuestionStatus.WAIT_FOR_ANSWER:
        question.status = QuestionStatus.ANSWERED

        database.commit()

        await update_question_message(event, question, user)

    await event.respond(
        SEND_ANSWER_SUCCESSFUL, buttons=Button.clear()
    )
