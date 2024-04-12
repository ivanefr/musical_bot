import sqlalchemy
from data.db_session import SqlAlchemyBase


class Tracks(SqlAlchemyBase):
    __tablename__ = 'tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    artist = sqlalchemy.Column(sqlalchemy.String, nullable=False)
