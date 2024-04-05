from shazamio import Shazam, Serialize
from shazamio.schemas.artists import ArtistInfo, ArtistV2
from shazamio.schemas.models import ResponseTrack

shazam = Shazam("RU")


class Artist:
    def __init__(self, data):
        self.__artist: ArtistInfo | ArtistV2 = Serialize.artist(data)

    @property
    def name(self):
        return self.__artist.name


class Track:
    def __init__(self, data):
        self.serialize = Serialize.track(data)

    @property
    def title(self):
        return self.serialize.title


class Recognizer:
    def __init__(self, data):
        self.data = data
        self.__full_track: ResponseTrack | None = None

    async def recognize_data(self):
        out = await shazam.recognize(data=self.data)
        self.__full_track = Serialize.full_track(out)
        print(self.__full_track)

    @property
    async def artist(self):
        artist_id = self.__full_track.track.artist_id
        if artist_id is None:
            return None
        artist_id = int(artist_id)
        artist_info = await shazam.artist_about(artist_id)
        artist = Artist(artist_info)
        return artist

    @property
    async def track(self):
        track_id = self.__full_track.track.key
        if track_id is None:
            return None
        track_id = int(track_id)
        track_info = await shazam.track_about(track_id)
        return Track(track_info)
