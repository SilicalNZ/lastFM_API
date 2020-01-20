from .query import UserQueries, ArtistQueries, AlbumQueries, TrackQueries


class LastFM_API:
    def __init__(self, api_key):
        self._api_key = api_key

    def get_user(self, user) -> UserQueries:
        return UserQueries(user, self._api_key)

    def get_artist(self, artist) -> ArtistQueries:
        return ArtistQueries(artist, self._api_key)

    def get_album(self, album, artist) -> AlbumQueries:
        return AlbumQueries(album, artist, self._api_key)

    def get_track(self, track, artist) -> TrackQueries:
        return TrackQueries(track, artist)