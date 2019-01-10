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




class Tagger():
    pass


class MapTrack(Tagger):
    """ [ Refer a Spotify track to Musicbrainz ]

        Steps:
        - Read a spotify track's info
        - Check if exists local mbz info
        - Request Musicbrainz API for track info
        - Make reference

    """

    def __init__(self, track):
        """
            Params:
            - track: [type] -> SpotifyTrack

            SQL:
            SELECT *,COUNT(*) AS c FROM ... WHERE type="track" GROUP BY real_uri HAVING c >1
        """
        pass

    @classmethod
    def mapTracks(cls, tracks):
        pass




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

    # Get track info
    track_uri = 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG'
    track, album, artist = test_get_track_info(track_uri)
    print( '\t', track.name, album.name, artist.name )

    # Check existence
    query = session.query(Reference).filter(
        Reference.uri == track_uri
    )
    print( '\t[REFs]', query.all() )
    refs = list(filter(lambda o: o.provider=='spotify', query.all()))
    spt = refs[0] if refs else None
    print( '\t[SPT]', spt )
    refs = list(filter(lambda o: o.provider=='musicbrainz', query.all()))
    mbz = refs[0] if refs else None
    print( '\t[MBZ]', mbz )

    if not mbz:
        results = MbzAPI.search_tracks(
            name=track.name, release=album.name, artist=artist.name,
        )
        # Filter out best match
        matches = sorted(results.get('recordings'),
            key=lambda o: o.get('score',0), reverse=True
        )
        best = matches[0] if matches else None
        # Add best match to database
        mbz = session.merge( MusicbrainzTrack(best) )
        print( '\t[BEST]', mbz )
        # Bind reference
        ref = Reference(mbz, spt.real_uri, mbz.score/100)
        print( '\t[BIND]', ref, ' at ', ref.real_uri )
        session.merge( ref )
        session.commit()

if __name__ == '__main__':
    main()





print('[  OK  ] __IMPORTED__: {}'.format(__name__))

