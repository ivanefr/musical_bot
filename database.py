from data import db_session
from data.recognized_track import RecognizedTrack

db_session.global_init("db/tracks.db")
db_sess = db_session.create_session()


def add_track(user_id, title, artist, album=None, genre=None, coverart_url=None, released=None):
    if not db_sess.query(RecognizedTrack).filter(RecognizedTrack.user_id == user_id,
                                                 RecognizedTrack.title == title,
                                                 RecognizedTrack.artist == artist).all():
        track = RecognizedTrack()
        track.user_id = user_id
        track.title = title
        track.artist = artist

        if album is not None:
            track.album = album

        if genre is not None:
            track.genre = genre

        if coverart_url is not None:
            track.coverart_url = coverart_url

        if released is not None:
            track.released = released

        db_sess.add(track)
        db_sess.commit()


def get_tracks(user_id):
    tracks = db_sess.query(RecognizedTrack).filter(RecognizedTrack.user_id == user_id).all()
    return tracks
