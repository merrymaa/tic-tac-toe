from sqlalchemy import create_engine, String, Column, ARRAY
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/game_db"
engine = create_engine(DATABASE_URL, echo=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    """"Объект SQLAlchemy - Users"""
    __tablename__ = "users"

    uuid: Mapped[str] = Column(String(40), primary_key=True, nullable=False)
    login: Mapped[str] = Column(String(40), unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)


class Games(Base):
    """"Объект SQLAlchemy - Games"""
    __tablename__ = "games"

    uuid = Column(String, primary_key=True, nullable=False)
    field = Column(ARRAY(String, dimensions=2), nullable=False)
    status = Column(String, default="waiting", nullable=False)  # waiting, active, finish
    type = Column(String, nullable=False)  # с человеком - HUMAN, с компьютером - AI
    step_player = Column(String, nullable=True)  # следующий ход игрока
    player_1_uuid = Column(String, nullable=True)  # UUID игрока за X
    player_2_uuid = Column(String, nullable=True)  # UUID игрока за O (для компьютера = "computer")
    player_1_sign = Column(CHAR, default="X")
    player_2_sign = Column(CHAR, default="O")
    draw = Column(String, nullable=True)  # ничья True / False
    winner = Column(String, nullable=True)  # победитель (если есть)


def init_db():
    Base.metadata.create_all(engine)


SessionLocal = sessionmaker(bind=engine)
