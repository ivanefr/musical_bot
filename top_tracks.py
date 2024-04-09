from shazamio import Shazam, Serialize

shazam = Shazam()


async def get_top_tracks_in_country(country_code, limit=10):
    top_tracks = await shazam.top_country_tracks(country_code, limit)
    return [Serialize.track(data=track) for track in top_tracks['tracks']]


async def get_top_world_tracks(limit=10):
    top_tracks = await shazam.top_world_tracks(limit)
    return [Serialize.track(data=track) for track in top_tracks['tracks']]
