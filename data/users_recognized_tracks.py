import sqlalchemy
from data.db_session import SqlAlchemyBase


class UsersRecognizedTracks(SqlAlchemyBase):
    __tablename__ = 'users_recognized_tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    artist = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    album = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    released = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coverart_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
