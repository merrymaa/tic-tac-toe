from sqlalchemy import create_engine, String, Column, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/game_db"
engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(40), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<User_id: {self.id}, user_name: {self.user_name}>"


class Games(Base):
    __tablename__ = "games"

    uuid = Column(String, primary_key=True, nullable=False)
    field = Column(ARRAY(String, dimensions=2), nullable=False)


def init_db():
    Base.metadata.create_all(engine)


SessionLocal = sessionmaker(bind=engine)

# session = SessionLocal()
# user_name = game_dto.user_info.name
# user_pass = game_dto.user_info.password_hash
#
# new_user = User(user_name=user_name, hashed_password=user_pass)
# session.add(new_user)
# session.commit()
# session.close()
