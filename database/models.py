from .constants import QuestionStatus
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text, Enum
from sqlalchemy.orm import declarative_base, relationship


DeclarativeBase = declarative_base()


class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True)
    full_name = Column(String)
    phone = Column(String, unique=True)
    active = Column(Boolean, default=True)

    admin = relationship(
        "Admins", back_populates="user", uselist=False, cascade="all, delete"
    )

    questions = relationship(
        "Questions", back_populates="user", cascade="all, delete"
    )

    @property
    def is_admin(self):
        return bool(self.admin)


class Admins(DeclarativeBase):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("Users", back_populates="admin")

    lessons = relationship("Lessons", back_populates="admin")


class Lessons(DeclarativeBase):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)

    admin_id = Column(ForeignKey("admins.id", ondelete="SET NULL"))
    admin = relationship("Admins", back_populates="lessons")

    questions = relationship("Questions", back_populates="lesson")


class Questions(DeclarativeBase):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(Text)
    status = Column(
        Enum(QuestionStatus), default=QuestionStatus.WAIT_FOR_ANSWER
    )
    created_at = Column(DateTime, server_default=func.now())

    lesson_id = Column(ForeignKey("lessons.id", ondelete="SET NULL"))
    lesson = relationship("Lessons", back_populates="questions")

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("Users", back_populates="questions")

    files = relationship(
        "Files", back_populates="question", cascade="all, delete"
    )


class Files(DeclarativeBase):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String)

    question_id = Column(ForeignKey("questions.id", ondelete="CASCADE"))
    question = relationship("Questions", back_populates="files")
