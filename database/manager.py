from .engine import SessionMaker
from .models import Users


class DatabaseManager:
    def __init__(self):
        self.session = SessionMaker()

    def create_user(self, **fields):
        user = Users(**fields)
        self.add(user)
        return user

    def get_user(self, **filters):
        return self.__get_users(**filters).first()

    def __get_users(self, **filters):
        return self.session.query(Users).filter_by(
            **filters
        ).order_by(Users.id)

    def add(self, model):
        self.session.add(model)

    def delete(self, model):
        self.session.delete(model)

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
