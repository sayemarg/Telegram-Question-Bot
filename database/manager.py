from .engine import SessionMaker
from .models import Users, Admins, Lessons


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

    def create_lesson(self, **fields):
        lesson = Lessons(**fields)
        self.add(lesson)
        return lesson

    def get_lesson(self, **filters):
        return self.__get_lessons(**filters).first()

    def get_lessons_count(self, **filters):
        return self.__get_lessons(**filters).count()

    def get_lessons_in_range(self, start, end, **filters):
        return self.__get_lessons(**filters)[start:end]

    def __get_lessons(self, **filters):
        return self.session.query(Lessons).filter_by(
            **filters
        ).order_by(Lessons.id)

    def add(self, model):
        self.session.add(model)

    def delete(self, model):
        self.session.delete(model)

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
