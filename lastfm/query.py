from functools import lru_cache
from time import time


import aiohttp
import asyncio

from .types import Tag, Album, Artist, User, Track


API_URL = 'http://ws.audioscrobbler.com/2.0/?'
RATE_LIMIT = 0.2
RATE_LIMIT_LAST_CALL = time()


async def request(query):
    global RATE_LIMIT_LAST_CALL
    global RATE_LIMIT


    if RATE_LIMIT_LAST_CALL + RATE_LIMIT > time():
        await asyncio.sleep(RATE_LIMIT)
        return await request(query)

    async with aiohttp.ClientSession() as session:
        async with session.get(query) as resp:
            assert resp.status == 200
            RATE_LIMIT_LAST_CALL = time()
            return await resp.json()


class Query:
    def __init__(self, base_string):
        self.base_string = base_string

    def modifiers(self, **kwargs):
        result = self.base_string
        for key, value in kwargs.items():
            result += f'&{key}={value}'
        return Query(result)

    def __repr__(self):
        return repr(self.base_string)

    def __str__(self):
        return str(self.base_string)


class Queries:
    method_modifier = None

    def __init__(self, api_key):
        self.api_url = Query(API_URL).modifiers(api_key=api_key, format='json')

    async def query(self, method, limit=1):  # Uncached requests
        query = str(self.api_url.modifiers(method=f'{self.method_modifier}.{method}', limit=limit))
        return await request(query)

    async def refined_query(self, method, cls, attrs, limit=1):
        responses = await self.query(method, limit)
        for attr in attrs:
            responses = responses.pop(attr)
        if isinstance(responses, dict):
            return cls(**responses)

        result =  [cls(**response) for response in responses]

        return result[0] if len(result) == 1 else result


class UserQueries(Queries):
    method_modifier = 'User'

    def __init__(self, username, api_key):
        super().__init__(api_key)
        self.api_url = self.api_url.modifiers(username=username)

    async def fetch_friends(self, limit=1):
        return await self.refined_query('getFriends', User, ('friends', 'user'), limit)

    async def fetch_info(self, limit=1):
        return await self.refined_query('getInfo', User, ('user', ), limit)

    async def fetch_loved_tracks(self, limit=1):
        return await self.refined_query('getLovedTracks', Track, ('lovedtracks', 'track'), limit)

    async def fetch_recent_tracks(self, limit=1):
        return await self.refined_query('getRecentTracks', Track, ('recenttracks', 'track'), limit)

    async def fetch_albums(self, limit=1):
        return await self.refined_query('getTopAlbums', Album, ('topalbums', 'album'), limit)

    async def fetch_artists(self, limit=1):
        return await self.refined_query('getTopArtists', Artist, ('topartists', 'artist'), limit)

    async def fetch_tags(self, limit=1):
        return await self.refined_query('getTopTags', Tag, ('toptags', 'tag'), limit)

    async def fetch_tracks(self, limit=1):
        return await self.refined_query('getTopTracks', Track, ('toptracks', 'track'), limit)

    async def fetch_weekly_albums(self, limit=1):
        return await self.refined_query('getWeeklyAlbumChart', Album, ('weeklyalbumchart', 'album'), limit)

    async def fetch_weekly_artists(self, limit=1):
        return await self.refined_query('getWeeklyArtistChart', Artist, ('weeklyartistchart', 'artist'), limit)

    async def fetch__weekly_charts(self):
        return await self.query('getWeeklyChartList')

    async def fetch_weekly_tracks(self, limit=1):
        return await self.refined_query('getWeeklyTrackChart', Track, ('weeklytrackchart', 'track'), limit)


class ArtistQueries(Queries):
    method_modifier = 'Artist'

    def __init__(self, artist, api_key):
        super().__init__(api_key)
        self.api_url = self.api_url.modifiers(artist=artist)
        self.artist = artist

    async def fetch_info(self, limit=1):
        return await self.refined_query('getInfo', Artist, ('artist', ), limit)

    async def fetch_similar(self, limit=1):
        return await self.refined_query('getSimilar', Artist, ('similarartists', 'artist'), limit)

    async def fetch_albums(self, limit=1):
        return await self.refined_query('getTopAlbums', Album, ('topalbums', 'album'), limit)

    async def fetch_tags(self, limit=1):
        return await self.refined_query('getTopTags', Tag, ('toptags', 'tag'), limit)

    async def fetch_tracks(self, limit=1):
        return await self.refined_query('getTopTracks', Track, ('toptracks', 'track'), limit)


class AlbumQueries(Queries):
    method_modifier = 'Album'

    def __init__(self, album, artist, api_key):
        super().__init__(api_key)
        self.api_url = self.api_url.modifiers(album=album, artist=artist)
        self.album = album
        self._api_key = api_key
        self._artist = artist

    @property
    @lru_cache()
    def artist(self):
        return ArtistQueries(self.artist, self._api_key)

    async def fetch_info(self, limit=1):
        return await self.refined_query('getInfo', Album, ('album', ), limit)

    async def fetch_tags(self, limit=1):
        return await self.refined_query('getTopTags', Tag, ('toptags', 'tag'), limit)


class TrackQueries(Queries):
    method_modifier = 'Track'

    def __init__(self, track, artist, api_key):
        super().__init__(api_key)
        self.api_url = self.api_url.modifiers(track=track, artist=artist)
        self.track = track
        self._artist = artist
        self._api_key = api_key

    @property
    @lru_cache()
    def artist(self):
        return ArtistQueries(self.artist, self._api_key)

    async def fetch_info(self, limit=1):
        return await self.refined_query('getInfo', Track, ('track', ), limit)

    async def fetch_similar(self, limit=1):
        return await self.refined_query('getSimilar', Track, ('similartracks', 'track'), limit)

    async def fetch_tags(self, limit=1):
        return await self.refined_query('getTopTags', Tag, ('toptags', 'tag'), limit)

