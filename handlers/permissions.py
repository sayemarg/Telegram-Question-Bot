from helpers import PROGRAMMER_CHAT_ID


def is_user_programmer(user):
    return user.chat_id == PROGRAMMER_CHAT_ID


def has_user_permission(user):
    return (user) and (user.active)


def has_admins_permission(user):
    return is_user_programmer(user) or (user.is_admin)
