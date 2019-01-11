#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json

from sqlalchemy import exists
from sqlalchemy.orm import aliased


#-> TEST only
if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
else:
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI



class MapTrack:
    """ [ Refer a Spotify track to Musicbrainz ]

        Steps:
        - Read a spotify track's info
        - Check if local mbz info exists
        - Request Musicbrainz API for track info
        - Make reference

    """

    def __init__(self, track_uri):
        """
            Params:
            - track_uri: [type] -> String
        """
        # Check track's references [Spotify] & [Musicbrainz]
        mbz,spt = self.check_references(track_uri)

        # Retrive tags from MBZ for this track if not exists
        if not mbz:
            # Get this track's info
            track, album, artist = self.get_track_info(track_uri)
            print( '\t', track.name, album.name, artist.name )
            # Tagging
            self.tag = mbz = self.tagging(spt.real_uri, track, album, artist)
            print( '[TAG]', mbz.name, mbz.uri )

    def check_references(self, track_uri):
        print('[NOW]__check_references__')
        query = session.query(Reference).filter(
            Reference.uri == track_uri
        )
        print( '\t[REFs]', query.all() )

        # Spotify
        refs = list(filter(lambda o: o.provider=='spotify', query.all()))
        spt = refs[0] if refs else None
        print( '\t[SPT]', spt )

        # Musicbrainz
        refs = list(filter(lambda o: o.provider=='musicbrainz', query.all()))
        mbz = refs[0] if refs else None
        print( '\t[MBZ]', mbz )

        return mbz, spt

    def get_track_info(self, track_uri):
        print('[NOW]__get_track_info__')
        # -> Middlewares for Many-to-Many tables
        trackAlbum = aliased(Include)
        trackArtists = aliased(Include)
        # -> Compose SQL
        query = session.query(
                SpotifyTrack, SpotifyAlbum, SpotifyArtist
                #Debug: SpotifyTrack.name, SpotifyAlbum.name, SpotifyArtist.name
            ).join(
                trackAlbum, SpotifyTrack.uri == trackAlbum.child_uri
            ).join(
                SpotifyAlbum, SpotifyAlbum.uri == trackAlbum.parent_uri
            ).join(
                trackArtists, SpotifyTrack.uri == trackArtists.child_uri
            ).join(
                SpotifyArtist, SpotifyArtist.uri == trackArtists.parent_uri
            ).filter(
                SpotifyTrack.uri == track_uri
            )
        # print( query.all().__len__(), query )
        # ->
        return query.first()

    def tagging(self, real_uri, track, album, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_track(
            name=track.name, release=album.name, artist=artist.name,
        )
        return MusicbrainzTrack.load( jsondata, real_uri )

    @classmethod
    def mapTracks(cls, uris):
        for uri in uris:
            tag = cls(uri)




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def test_get_track_info(track_uri):
    # Compose SQL
    # -> Middlewares for Many-to-Many tables
    trackAlbum = aliased(Include)
    trackArtists = aliased(Include)
    # -> Query
    query = session.query(
            SpotifyTrack, SpotifyAlbum, SpotifyArtist
            #Debug: SpotifyTrack.name, SpotifyAlbum.name, SpotifyArtist.name
        ).join(
            trackAlbum, SpotifyTrack.uri == trackAlbum.child_uri
        ).join(
            SpotifyAlbum, SpotifyAlbum.uri == trackAlbum.parent_uri
        ).join(
            trackArtists, SpotifyTrack.uri == trackArtists.child_uri
        ).join(
            SpotifyArtist, SpotifyArtist.uri == trackArtists.parent_uri
        ).filter(
            SpotifyTrack.uri == track_uri
        )
    # print( query, query.all().__len__() )
    # ->
    return query.first()




def main():
    track_uri = 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG'
    tag = MapTrack(track_uri)



if __name__ == '__main__':
    main()





print('[  OK  ] __IMPORTED__: {}'.format(__name__))

