from enum import Enum


class QuestionStatus(Enum):
    WAIT_FOR_ANSWER = 0
    ANSWERED = 1
    CANCELED = 2
    REMOVED = 3
