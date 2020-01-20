from datetime import datetime
from time import time
import asyncio

from .utils import popconvert


class BaseType:
    def __iadd__(self, other):
        [setattr(self, slot, getattr(other, name))
         for slot, name in zip(self.__slots__, other.__slots__)
         if getattr(self, slot) is not None]

    def __repr__(self):
        return repr({slot: getattr(self, slot) for slot in self.__slots__})


class Image:
    __slots__ = 'small', 'medium', 'large', 'extralarge', 'mega'

    def __init__(self, images):
        [setattr(self, *size.values()) for size in images]

    def images(self):
        return tuple(slot for slot in self.__slots__ if getattr(self, slot) is not None)


class Tag(BaseType):
    __slots__ = 'count', 'name', 'url'

    def __init__(self, **kwargs):
        self.count = popconvert(kwargs, 'count', int)
        self.name = popconvert(kwargs, 'name')
        self.url = popconvert(kwargs, 'url')


class Artist(BaseType):
    __slots__ = 'mbid', 'name', 'url', 'playcount', 'image', \
            'streamable', 'bio', 'ontour', 'stats', 'tags'

    def __init__(self, **kwargs):
        self.image = popconvert(kwargs, 'image', Image)
        self.streamable = popconvert(kwargs, 'streamable')
        self.playcount = popconvert(kwargs, 'playcount', int)
        self.mbid = popconvert(kwargs, 'mbid')
        self.name = popconvert(kwargs, 'name')
        self.url = popconvert(kwargs, 'url')
        self.bio = popconvert(kwargs, 'bio')
        self.ontour = popconvert(kwargs, 'ontour')
        self.stats = popconvert(kwargs, 'stats')
        self.tags = popconvert(kwargs, 'tags')


class User(BaseType):
    __slots__ = 'bootstrap', 'country', 'image', 'name', 'playcount', 'playlists', \
            'realname', 'registered', 'subscriber', 'type', 'url', 'age', \
            'gender'

    def __init__(self, **kwargs):
        self.bootstrap = popconvert(kwargs, 'bootstrap')
        self.country = popconvert(kwargs, 'country')
        self.image = popconvert(kwargs, 'image', Image)
        self.name = popconvert(kwargs, 'name')
        self.playcount = popconvert(kwargs, 'playcount', int)
        self.playlists = popconvert(kwargs, 'playlists', int)
        self.realname = popconvert(kwargs, 'realname')
        self.registered = popconvert(kwargs, 'registered')
        if self.registered:
            self.registered = int(self.registered['unixtime'])

        self.subscriber = popconvert(kwargs, 'subscriber', int)
        self.type = popconvert(kwargs, 'type')
        self.url = popconvert(kwargs, 'url')
        self.age = popconvert(kwargs, 'age', int)
        self.gender = popconvert(kwargs, 'gender')

    @property
    def registered_at(self):
        if self.registered:
            return datetime.utcfromtimestamp(self.registered)


class Track(BaseType):
    __slots__ = 'date', 'streamable', 'artist', 'image', 'mbid', \
            'name', 'playcount', 'url', 'listeners', 'duration', \
            'album'

    def __init__(self, **kwargs):
        self.streamable = popconvert(kwargs, 'streamable')
        self.date = popconvert(kwargs, 'date')
        if self.date:
            self.date =int(self.date['uts'])
        self.artist = popconvert(kwargs, 'artist', Artist)
        self.image = popconvert(kwargs, 'image', Image)
        self.mbid = popconvert(kwargs, 'mbid')
        self.name = popconvert(kwargs, 'name')
        self.playcount = popconvert(kwargs, 'playcount')
        self.url = popconvert(kwargs, 'url')
        self.listeners = popconvert(kwargs, 'listeners', int)
        self.duration = popconvert(kwargs, 'duration', int)
        self.album = popconvert(kwargs, 'album', Album)

    @property
    def date_at(self):
        if self.date:
            return datetime.utcfromtimestamp(self.date)


class Album(BaseType):
    __slots__ = 'image', 'artist', 'mbid', 'name', 'playcount', \
            'url', 'tags', 'listeners', 'tracks'

    def __init__(self, **kwargs):
        self.image = popconvert(kwargs, 'image', Image)
        self.artist = popconvert(kwargs, 'artist')
        self.mbid = popconvert(kwargs, 'mbid')
        self.name = popconvert(kwargs, 'name')
        self.playcount = popconvert(kwargs, 'playcount', int)
        self.url = popconvert(kwargs, 'url')
        self.tags = popconvert(kwargs, 'tags')
        self.listeners = popconvert(kwargs, 'listeners', int)
        self.tracks = popconvert(kwargs, 'tracks')
