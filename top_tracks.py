import asyncio
from shazamio import Shazam, Serialize


async def get_top_tracks_in_country(country_code, limit=10):
    shazam = Shazam()
    top_tracks = await shazam.top_country_tracks(country_code, limit)
    return [Serialize.track(data=track) for track in top_tracks['tracks']]


async def get_top_world_tracks(limit=10):
    shazam = Shazam()
    top_tracks = await shazam.top_world_tracks(limit)
    return [Serialize.track(data=track) for track in top_tracks['tracks']]


def run_top_tracks():
    loop = asyncio.get_event_loop()
    top_tracks_russia = loop.run_until_complete(get_top_tracks_in_country('RU'))
    top_tracks_world = loop.run_until_complete(get_top_world_tracks())
    return top_tracks_russia, top_tracks_world
