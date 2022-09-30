from handlers.constants import CONVERSATION_TIMEOUT
from math import ceil
from messages.globals import CHOOSE_FROM_BUTTONS, SKIP_BUTTON, REASON_LENGTH_LIMIT
from messages.pagination import *
from telethon import Button


async def get_user_confirm(
    bot, chat_id, confirm_message, yes_button, no_button, cancel_message
):
    async with bot.conversation(
        chat_id, timeout=CONVERSATION_TIMEOUT
    ) as conversation:
        await conversation.send_message(
            confirm_message,
            buttons=[
                [Button.text(
                    yes_button, resize=True, single_use=True
                )],
                [Button.text(
                    no_button, resize=True, single_use=True
                )],
            ]
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == yes_button:
                return True

            elif response.raw_text == no_button:
                await conversation.send_message(
                    cancel_message,
                    buttons=Button.clear()
                )
                return

            await conversation.send_message(CHOOSE_FROM_BUTTONS)


async def get_reason_from_user(
    bot, chat_id, send_reason_message, reason_max_length, cancel_message,
    not_empty_message, reason_skipped_message
):
    async with bot.conversation(
        chat_id, timeout=CONVERSATION_TIMEOUT
    ) as conversation:
        await conversation.send_message(
            send_reason_message.format(reason_max_length),
            buttons=Button.text(SKIP_BUTTON, resize=True, single_use=True)
        )

        while True:
            response = await conversation.get_response()

            if response.raw_text == "/cancel":
                await conversation.send_message(
                    cancel_message,
                    buttons=Button.clear()
                )
                return

            if not response.raw_text:
                await conversation.send_message(not_empty_message)
                continue

            if reason_max_length < len(response.raw_text):
                await conversation.send_message(
                    REASON_LENGTH_LIMIT.format(reason_max_length)
                )
                continue

            return reason_skipped_message if (
                response.raw_text == SKIP_BUTTON
            ) else response.raw_text


def create_list_message(
    list_items, total_count, start, item_text, format_item_function
):
    index, counter = 0, start

    list_length = len(list_items)

    list_text = ""

    while True:
        item = list_items[index]

        counter += 1

        list_text += item_text.format(*format_item_function(counter, item))

        index += 1

        if list_length <= index:
            break

        list_text += LIST_DELIMETER

    return PAGINATION_LIST_MESSAGE.format(total_count, list_text)


def generate_pagination_buttons(command_prefix, page_length, page_number, list_length):
    page_counter = ceil(list_length / page_length)

    (
        buttons, next_previous_buttons, five_next_previous_buttons,
        first_last_page_buttons
    ) = [], [], [], []

    if 1 < page_number:
        next_previous_buttons.append(
            Button.inline(
                PREVIOUS_PAGE_BUTTON, f"{command_prefix}{page_number - 1}"
            )
        )

        first_last_page_buttons.append(
            Button.inline(FIRST_PAGE, f"{command_prefix}1")
        )

    if page_number < page_counter:
        next_previous_buttons.append(
            Button.inline(
                NEXT_PAGE_BUTTON, f"{command_prefix}{page_number + 1}"
            )
        )

        first_last_page_buttons.append(
            Button.inline(LAST_PAGE, f"{command_prefix}{page_counter}")
        )

    if 5 < page_number:
        five_next_previous_buttons.append(
            Button.inline(
                PREVIOUS_5_PAGE_BUTTON, f"{command_prefix}{page_number - 5}"
            )
        )

    if (page_number + 5) <= page_counter:
        five_next_previous_buttons.append(
            Button.inline(
                NEXT_5_PAGE_BUTTON, f"{command_prefix}{page_number + 5}"
            )
        )

    if next_previous_buttons:
        buttons.append(next_previous_buttons)

    if five_next_previous_buttons:
        buttons.append(five_next_previous_buttons)

    if first_last_page_buttons:
        buttons.append(first_last_page_buttons)

    return (buttons or None)
