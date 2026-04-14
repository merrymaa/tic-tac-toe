from sqlalchemy import create_engine, String, Column, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker

# from sqlalchemy.exc import OperationalError

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

    def __repr__(self):
        return f"<User_id: {self.uuid}, user_name: {self.login}>"


class Games(Base):
    """"Объект SQLAlchemy - Games"""
    __tablename__ = "games"

    uuid = Column(String, primary_key=True, nullable=False)
    field = Column(ARRAY(String, dimensions=2), nullable=False)


def init_db():
    Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)


