from database import QuestionStatus


QUESTION_NOT_FOUND = """
ما همچین سوالی را پیدا نکرده ایم 🤷‍♂️.
ممکن است خطایی رخ داده باشد یا این سوال حذف شده باشد.
لطفا داده های خود را به روزرسانی کنید.
"""

QuestionStatusText = {
    QuestionStatus.WAIT_FOR_ANSWER: "🕐 در انتظار پاسخ",
    QuestionStatus.ANSWERED: "📬 پاسخ داده شده",
}

QUESTION_TEXT = """
{}- /question_detail_{}

عنوان: **{}**
درس: **{}**

**{}**
"""
