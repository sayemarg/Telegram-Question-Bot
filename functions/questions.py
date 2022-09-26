from database import QuestionStatus
from messages.globals.questions import QuestionStatusText
from messages.shared.question_detail import (
    QUESTION_DETAIL_TEXT, DELETED_LESSON_TITLE, DELETE_QUESTION_BUTTON,
    ADD_FILE_BUTTON, ANSWER_QUESTION_BUTTON, REANSWER_QUESTION_BUTTON,
    QUESTION_FILES_BUTTON
)
from telethon import Button


def format_question_lesson_name(question):
    return question.lesson.title if question.lesson else DELETED_LESSON_TITLE


def format_question_preview_function(counter, question): return (
    counter,
    question.id,
    question.title,
    format_question_lesson_name(question),
    QuestionStatusText[question.status]
)


def generate_question_message_and_buttons(question, user, is_admin):
    buttons = [
        [Button.inline(
            DELETE_QUESTION_BUTTON, f"/delete_question_{question.id}"
        )],
    ]

    second_row_buttons = [
        Button.inline(
            QUESTION_FILES_BUTTON, f"/question_attachments_{question.id}"
        )
    ]

    if question.user_id == user.id:
        second_row_buttons.append(
            Button.inline(
                ADD_FILE_BUTTON, f"/attach_file_{question.id}"
            )
        )

    buttons.append(second_row_buttons)

    if is_admin:
        button_text = ANSWER_QUESTION_BUTTON if (
            question.status == QuestionStatus.WAIT_FOR_ANSWER
        ) else REANSWER_QUESTION_BUTTON

        buttons.append([
            Button.inline(button_text, f"/answer_question_{question.id}")
        ])

    return QUESTION_DETAIL_TEXT.format(
        question.title,
        question.user.full_name,
        format_question_lesson_name(question),
        question.text,
        QuestionStatusText[question.status]
    ), buttons
