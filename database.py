from data import db_session
from data.users_recognized_tracks import UsersRecognizedTracks
from data.tracks import Tracks
from data.users import Users

db_session.global_init("db/shazam.db")
db_sess = db_session.create_session()


def add_user(user_id):
    if not db_sess.query(Users).filter(Users.user_id == user_id).all():
        user = Users()
        user.user_id = user_id

        db_sess.add(user)
        db_sess.commit()


def add_track(user_id, title, artist, album=None, genre=None, coverart_url=None, released=None):
    if not db_sess.query(Tracks).filter(Tracks.title == title,
                                        Tracks.artist == artist).all():
        track = Tracks()
        track.title = title
        track.artist = artist

        db_sess.add(track)
        db_sess.commit()
    if not db_sess.query(UsersRecognizedTracks).filter(UsersRecognizedTracks.user_id == user_id,
                                                       UsersRecognizedTracks.title == title,
                                                       UsersRecognizedTracks.artist == artist).all():
        track = UsersRecognizedTracks()
        track.user_id = user_id
        track.title = title
        track.artist = artist
        track.album = album
        track.genre = genre
        track.coverart_url = coverart_url
        track.released = released

        db_sess.add(track)
        db_sess.commit()


def get_users_tracks(user_id):
    tracks = db_sess.query(UsersRecognizedTracks).filter(UsersRecognizedTracks.user_id == user_id).all()
    return tracks


def get_count_tracks():
    tracks = db_sess.query(Tracks).all()
    return len(tracks)


def get_count_users():
    users = db_sess.query(Users).all()
    return len(users)
