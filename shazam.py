from shazamio import Shazam, Serialize


class Song:
    def __init__(self, data):
        self.data = data
        self.file_path = "voice.mp3"
        self.__shazam = Shazam(language="ru-RU")
        self.__out = None
        self.__artist = None
        self.__title = None

    async def recognize_data(self):
        self.__out = await self.__shazam.recognize(data=self.data)
        serialize = Serialize.full_track(self.__out)
        track = serialize.track
        if track is not None:
            self.__artist = track.subtitle
            self.__title = track.title

    @property
    def artist(self):
        return self.__artist

    @property
    def title(self):
        return self.__title
