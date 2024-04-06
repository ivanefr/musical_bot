import sqlalchemy
from data.db_session import SqlAlchemyBase


class RecognizedTrack(SqlAlchemyBase):
    __tablename__ = 'recognized_track'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    artist = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    album = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    released = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coverart_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)


