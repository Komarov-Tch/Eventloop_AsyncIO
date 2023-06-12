import sqlalchemy
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
load_dotenv()

PG_DSN = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@127.0.0.1:5431/{os.getenv('POSTGRES_DB')}"
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
    )


class SWPeople:

    __tablename__ = 'people'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    birth_year = sqlalchemy.Column(sqlalchemy.String)
    eye_color = sqlalchemy.Column(sqlalchemy.String)
    films = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.String)
    hair_color = sqlalchemy.Column(sqlalchemy.String)
    height = sqlalchemy.Column(sqlalchemy.String)
    homeworld = sqlalchemy.Column(sqlalchemy.String)
    mass = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    skin_color = sqlalchemy.Column(sqlalchemy.String)
    species = sqlalchemy.Column(sqlalchemy.String)
    starships = sqlalchemy.Column(sqlalchemy.String)
    vehicles = sqlalchemy.Column(sqlalchemy.String)
