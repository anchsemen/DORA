from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, ForeignKey, Text

database_url = 'sqlite:///data/sqlite.db'
engine = create_engine(database_url)
async_engine = create_async_engine("sqlite+aiosqlite:///data/sqlite.db")
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    user_email = Column(String(255), nullable=False)
    hash_password = Column(String(255), nullable=False, unique=True)


class DBCharacters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), nullable=False)
    sex = Column(Integer, nullable=False)
    age = Column(String(255), nullable=False)
    path_to_doc = Column(String(255), nullable=False)


class DBCommunication(Base):
    __tablename__ = "communication"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_msg = Column(Text)
    bot_msg = Column(Text)


def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
