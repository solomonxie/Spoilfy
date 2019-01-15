#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
from time import sleep

from sqlalchemy import exists
from sqlalchemy.orm import aliased


#-> TEST only
if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    from webapi.apiMusicbrainz import MusicbrainzAPI as MbzAPI
    from mbzOps import MbzOpsTrack, MbzOpsAlbum, MbzOpsArtist
else:
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    from Spoilfy.webapi.apiMusicbrainz import MusicbrainzAPI as MbzAPI


class Mapper:
    """ [ Map Spotify item to Musicbrainz ]

        Steps:
        - Read a spotify item's info
        - Check if related local mbz info exists
        - Request Musicbrainz API for the info
        - Save the best match to Database
    """

    @classmethod
    def get_references(cls, uri):
        refs = {}

        print('[NOW]__get_references__')
        real_uri = session.query(Reference).filter(
            Reference.uri == uri
        ).first().real_uri
        results = session.query(Reference).filter(
            Reference.real_uri == real_uri
        ).all()
        print( '[QUERY]', results )

        # Spotify
        r = list(filter(lambda o: o.provider=='spotify', results))
        refs['spotify'] = r[0] if r else None
        # Musicbrainz
        r = list(filter(lambda o: o.provider=='musicbrainz', results))
        refs['musicbrainz'] = r[0] if r else None
        print( '\t[REFs]', refs )

        return refs

    @classmethod
    def toMbz(cls, uri):
        print( '[toMbz()] TO BE IMPLEMENTED' )

    @classmethod
    def get_spotify_info(cls, uri):
        print( '[get_spotify_info()] TO BE IMPLEMENTED' )

    @classmethod
    def get_musicbrainz_info(cls, real_uri, **query):
        print( '[get_musicbrainz_info()] TO BE IMPLEMENTED' )

    @classmethod
    def mapItems(cls, uris):
        for uri in uris:
            tag = cls(uri)



class MapTrack(Mapper):
    """ [ Map a Spotify track to Musicbrainz ]
    """

    @classmethod
    def toMbz(cls, uri):
        """
            Params:
            - uri [type:String]: spotify track's uri
        """
        # Check track's references [Spotify] & [Musicbrainz]
        refs = cls.get_references( uri )
        spt = refs.get('spotify')
        mbz = refs.get('musicbrainz')
        if spt and mbz:
            print( '[SKIP] TAGs FOUND.' )
            return mbz

        # Retrive tags from MBZ for this track if not exists
        info = cls.get_spotify_info( uri ) if not mbz else None
        if info:
            track, album, artist = info
            print( '\t', track.name, album.name, artist.name )

            # Tagging
            print('[NOW]__tagging__')
            jsondata = MbzAPI.best_match_track(
                name=track.name, release=album.name, artist=artist.name,
            )
            sleep(1)
            if jsondata:
                mbz =  MbzOpsTrack.load( jsondata, spt.real_uri )
                return mbz
            else:
                print( '[SKIP] NO TAG FOUND.' )
        else:
            print( '[SKIP] SPT INFO INCOMPLETE.' )
            sleep(3)


    @classmethod
    def get_spotify_info(cls, uri):
        print('[NOW]__get_spt_info__:{}'.format(uri))

        # -> Middlewares for Many-to-Many tables
        trackAlbum = aliased(Include)
        trackArtists = aliased(Include)

        # Query this track and its album from DB
        info = session.query(
            SpotifyTrack, SpotifyAlbum
        ).filter(
            SpotifyTrack.uri == uri,
            SpotifyTrack.uri == trackAlbum.child_uri,
            SpotifyAlbum.uri == trackAlbum.parent_uri
        ).first()
        track, album = info if info else (None, None)

        # Query track's artist from DB
        info = session.query(
            SpotifyArtist
        ).filter(
            SpotifyTrack.uri == uri,
            SpotifyTrack.uri == trackArtists.child_uri,
            SpotifyArtist.uri == trackArtists.parent_uri
        ).first()
        artist = info if info else None

        print('(track, album, artist):', track, album, artist)
        return (track, album, artist) if track and album and artist else None

    @classmethod
    def get_musicbrainz_info(cls, real_uri, track, album, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_track(
            name=track.name, release=album.name, artist=artist.name,
        )
        return MusicbrainzTrack.load( jsondata, real_uri )



class MapAlbum(Mapper):
    """ [ Map a Spotify album to Musicbrainz ]
    """

    @classmethod
    def toMbz(cls, uri):
        """
            Params:
            - uri [type:String]: spotify album's uri
        """
        # Check track's references [Spotify] & [Musicbrainz]
        mbz,spt = cls.get_references( uri )

        # Retrive tags from MBZ for this album if not exists
        if not mbz:
            # Get this track's info
            album, artist = cls.get_spotify_info( uri )
            print( '\t', album.name, artist.name )
            # Tagging
            mbz = cls.get_musicbrainz_info(spt.real_uri, album, artist)
            print( '[  TAG  ]', mbz.name, mbz.uri )

    @classmethod
    def get_spotify_info(cls, uri):
        print('[NOW]__get_spotify_album_info__')
        # -> Middlewares for Many-to-Many tables
        albumArtists = aliased(Include)
        # -> Compose SQL
        query = session.query(
                SpotifyAlbum, SpotifyArtist
                #Debug: SpotifyAlbum.name, SpotifyArtist.name
            ).join(
                albumArtists, SpotifyAlbum.uri == albumArtists.child_uri
            ).filter(
                SpotifyArtist.uri == albumArtists.parent_uri,
                SpotifyAlbum.uri == uri
            )
        # print( query.all().__len__(), query )
        # ->
        return query.first()

    @classmethod
    def get_musicbrainz_info(cls, real_uri, album, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_album(
            name=album.name, artist=artist.name,
        )
        mbz = MusicbrainzAlbum.load( jsondata, real_uri )
        return mbz



class MapArtist(Mapper):
    """ [ Map a Spotify artist to Musicbrainz ]
    """

    @classmethod
    def toMbz(cls, uri):
        """
            Params:
            - uri [type:String]: spotify artist's uri
        """
        # Check track's references [Spotify] & [Musicbrainz]
        mbz,spt = cls.get_references( uri )

        # Retrive tags from MBZ for this album if not exists
        if not mbz:
            # Get this track's info
            artist = cls.get_spotify_info( uri )
            print( '\t', artist.name )
            # Tagging
            mbz = cls.get_musicbrainz_info(spt.real_uri, artist)
            print( '[  TAG  ]', mbz.name, mbz.uri )

    @classmethod
    def get_spotify_info(cls, uri):
        print('[NOW]__get_spotify_artist_info__')
        # -> Middlewares for Many-to-Many tables
        albumArtists = aliased(Include)
        # -> Compose SQL
        query = session.query( SpotifyArtist ).filter(
            SpotifyArtist.uri == uri
        )
        # print( query.all().__len__(), query )
        # ->
        return query.first()

    @classmethod
    def get_musicbrainz_info(cls, real_uri, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_artist(
            name=artist.name
        )
        print( jsondata )
        mbz = MusicbrainzArtist.load( jsondata, real_uri )
        return mbz




print('[  OK  ] __IMPORTED__: {}'.format(__name__))

