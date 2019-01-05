#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:


from sqlalchemy import exists


#-> TEST only
if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.spotify import SpotifyAPI
    import webapi.musicbrainz as mba
else:
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.spotify import SpotifyAPI
    import Spoilfy.webapi.musicbrainz as mba




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


def main():
    # results = session.query(
        # Reference, Reference.real_uri, Reference.nlinked
    # ).filter(
        # Reference.type == 'track',
        # # Reference.nlinked < 2 # ->Filter out untagged tracks
    # )
    # print( results )
    # for r in results:
        # r[0].nlinked += 1
        # session.commit()
        # print( '[  OK  ]',r )
    import json
    # Get track info
    track_uri = 'spotify:track:4BXos4QJgyEF3dytRNNytV'
    # ========
    # =>TODO<= merge two queries to one
    # ========
    track, album = session.query(SpotifyTrack, SpotifyAlbum).filter(
        SpotifyTrack.uri == track_uri,
        Include.child_uri == track_uri,
        Include.parent_uri == SpotifyAlbum.uri,
    ).first()
    artist = session.query(SpotifyArtist).filter(
        Include.child_uri == track.uri,
        Include.parent_uri == SpotifyArtist.uri
    ).first()
    print('Track:[{}], Album:[{}], Artist:[{}]'.format(
        track.name, album.name, artist.name
    ))
    # Check existence
    tag = session.query(Reference.uri).filter(
        Reference.uri == track_uri,
        Reference.provider == 'musicbrainz'
    ).first()
    print( '[  TAG  ]',tag )
    # Request MBZ WebAPI
    if not tag:
        results = mba.search_tracks(
            name=track.name,
            release=album.name,
            artist=artist.name,
        )
        for obj in results.get('recordings'):
            print('\t[TRACK]:',
                obj.get('title'), obj.get('score'),
                obj.get('artist-credit')[0].get('artist').get('name')
            )
    # Make reference

if __name__ == '__main__':
    main()





print('[  OK  ] __IMPORTED__: {}'.format(__name__))

