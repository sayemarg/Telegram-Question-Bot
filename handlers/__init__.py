from .admins.activate_user import activate_user_handler
from .admins.add_lesson import add_lesson_handler
from .admins.deactivate_user import deactivate_user_handler
from .admins.delete_lesson import delete_lesson_handler
from .admins.downgrade_admin import downgrade_admin_handler
from .admins.lesson_detail import lesson_detail_handler
from .admins.lessons_list import lessons_list_handler
from .admins.questions_list import all_questions_list_handler
from .admins.upgrade_user import upgrade_user_handler
from .admins.user_detail import user_detail_handler
from .admins.users_list import users_list_handler
from .shared.main_menu import main_menu_handler
from .shared.question_detail import question_detail_handler
from .shared.start import start_handler
from .users.add_question import add_question_handler
from .users.my_questions import my_questions_list_handler


BOT_EVENT_HANDLERS = [
    activate_user_handler,
    add_lesson_handler,
    add_question_handler,
    all_questions_list_handler,
    deactivate_user_handler,
    delete_lesson_handler,
    downgrade_admin_handler,
    lesson_detail_handler,
    lessons_list_handler,
    main_menu_handler,
    my_questions_list_handler,
    question_detail_handler,
    start_handler,
    upgrade_user_handler,
    user_detail_handler,
    users_list_handler,
]
