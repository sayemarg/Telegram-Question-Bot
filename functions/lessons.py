from messages.admins.lesson_detail import (
    DELETE_LESSON_BUTTON, SHOW_LESSON_QUESTIONS_BUTTON, LESSON_DETAIL_TEXT
)
from telethon import Button


def format_lesson_preview_function(counter, lesson): return (
    counter,
    lesson.id,
    lesson.title,
)


def generate_lesson_message_and_buttons(lesson):
    buttons = [
        [Button.inline(
            SHOW_LESSON_QUESTIONS_BUTTON, f"/lesson_questions_{lesson.id}_1"
        )],
        [Button.inline(DELETE_LESSON_BUTTON, f"/delete_lesson_{lesson.id}")]
    ]

    return LESSON_DETAIL_TEXT.format(
        lesson.title
    ), buttons
