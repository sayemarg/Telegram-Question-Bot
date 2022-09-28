from .constants import QuestionStatus
from .engine import SessionMaker
from .models import Users, Admins, Lessons, Questions, Attachments


class DatabaseManager:
    def __init__(self):
        self.session = SessionMaker()

    def create_user(self, **fields):
        user = Users(**fields)
        self.add(user)
        return user

    def get_user(self, **filters):
        return self.__get_users(**filters).first()

    def get_users_count(self, **filters):
        return self.__get_users(**filters).count()

    def get_users_in_range(self, start, end, **filters):
        return self.__get_users(**filters)[start:end]

    def __get_users(self, **filters):
        return self.session.query(Users).filter_by(
            **filters
        ).order_by(Users.id)

    def create_admin(self, **fields):
        admin = Admins(**fields)
        self.add(admin)
        return admin

    def get_admins_list(self, **filters):
        return self.session.query(Admins).filter_by(
            **filters
        ).all()

    def create_lesson(self, **fields):
        lesson = Lessons(**fields)
        self.add(lesson)
        return lesson

    def get_lesson(self, **filters):
        return self.__get_lessons(**filters).first()

    def get_lessons_list(self, **filters):
        return self.__get_lessons(**filters).all()

    def get_lessons_count(self, **filters):
        return self.__get_lessons(**filters).count()

    def get_lessons_in_range(self, start, end, **filters):
        return self.__get_lessons(**filters)[start:end]

    def __get_lessons(self, **filters):
        return self.session.query(Lessons).filter_by(
            **filters
        ).order_by(Lessons.id)

    def create_question(self, **fields):
        question = Questions(**fields)
        self.add(question)
        return question

    def get_question(self, **filters):
        return self.__get_questions(**filters).first()

    def get_questions_count(self, **filters):
        return self.__get_questions(**filters).count()

    def get_questions_in_range(self, start, end, **filters):
        return self.__get_questions(**filters)[start:end]

    def __get_questions(self, **filters):
        return self.session.query(Questions).filter_by(**filters).filter(
            Questions.status != QuestionStatus.CANCELED,
            Questions.status != QuestionStatus.REMOVED,
        ).order_by(Questions.id.desc())

    def create_attachment(self, **fields):
        attachment = Attachments(**fields)
        self.add(attachment)
        return attachment

    def get_attachments_count(self, **filters):
        return self.__get_attachments(**filters).count()

    def get_attachments_list(self, **filters):
        return self.__get_attachments(**filters).all()

    def __get_attachments(self, **filters):
        return self.session.query(Attachments).filter_by(
            **filters
        ).order_by(Attachments.id)

    def add(self, model):
        self.session.add(model)

    def delete(self, model):
        self.session.delete(model)

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
