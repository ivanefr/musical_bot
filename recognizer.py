from shazamio import Shazam, Serialize
from shazamio.schemas.models import ResponseTrack

shazam = Shazam("RU")


class Track:
    def __init__(self, data):
        self.data = data
        self.__full_track: ResponseTrack | None = None
        self.__out = {}

    async def recognize_data(self):
        self.__out = await shazam.recognize(data=self.data)
        self.__full_track = Serialize.full_track(self.__out)

    @property
    def title(self):
        if self.__full_track.track is not None:
            return self.__full_track.track.title
        return None

    @property
    def artist(self):
        return self.__full_track.track.subtitle

    @property
    def album(self):
        try:
            album = self.__out["track"]["sections"][0]["metadata"][0]["text"]
        except IndexError:
            return None
        except KeyError:
            return None
        return album

    @property
    def released(self):
        try:
            date = self.__out["track"]["sections"][0]["metadata"][-1]["text"]
        except IndexError:
            return None
        except KeyError:
            return None
        return date

    @property
    def genre(self):
        try:
            genre = self.__out["track"]["genres"]["primary"]
        except IndexError:
            return None
        except KeyError:
            return None
        return genre

    @property
    def coverart_url(self):
        try:
            url = self.__out["track"]["sections"][0]["metapages"][1]["image"]
        except IndexError:
            return None
        except KeyError:
            return None
        return url
