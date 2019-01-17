#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
from time import sleep

from sqlalchemy import exists
from sqlalchemy.orm import aliased
from sqlalchemy import text


#-> TEST only
if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import *
    from orm.musicbrainz import *
    from orm.common import Base, engine, session, Resource
    from orm.common import Reference, Include, UnTagged, Incomplete
    from webapi.apiSpotify import SpotifyAPI
    from webapi.apiMusicbrainz import MusicbrainzAPI as MbzAPI
    from mbzOps import MbzOpsTrack, MbzOpsAlbum, MbzOpsArtist
else:
    from Spoilfy.orm.spotify import *
    from Spoilfy.orm.musicbrainz import *
    from Spoilfy.orm.common import Base, engine, session, Resource
    from Spoilfy.orm.common import Reference, Include, UnTagged, Incomplete
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    from Spoilfy.webapi.apiMusicbrainz import MusicbrainzAPI as MbzAPI



TB_SPT_TK = SpotifyTrack.__tablename__
TB_SPT_AB = SpotifyAlbum.__tablename__
TB_SPT_AT = SpotifyArtist.__tablename__
TB_SPT_PL = SpotifyPlaylist.__tablename__

class UnMapped:

    @classmethod
    def _find_unmapped(cls, sql):
        with engine.connect() as con:
            records = con.execute(sql)
            uris = [ u for u, in records ]
        return uris

    @classmethod
    def find_unmapped_tracks(cls):
        return cls._find_unmapped(
            """
            SELECT uri FROM 'references'
                WHERE provider='spotify' AND type='track'
                AND real_uri NOT IN
                (
                    SELECT real_uri FROM 'references'
                        WHERE type='track' AND provider='musicbrainz'
                )
                AND real_uri NOT IN (SELECT real_uri from '_untagged')
                AND real_uri NOT IN (SELECT real_uri from '_incompletes')
            """
        )

    @classmethod
    def find_unmapped_albums(cls):
        return cls._find_unmapped(
            """
            SELECT uri FROM 'references'
                WHERE provider='spotify' AND type='album'
                AND real_uri NOT IN
                (
                    SELECT real_uri FROM 'references'
                        WHERE type='album' AND provider='musicbrainz'
                )
                AND real_uri NOT IN (SELECT real_uri from '_untagged')
                AND real_uri NOT IN (SELECT real_uri from '_incompletes')
            """
        )

    @classmethod
    def find_unmapped_artists(cls):
        return cls._find_unmapped(
            """
            SELECT uri FROM 'references'
                WHERE provider='spotify' AND type='artist'
                AND real_uri NOT IN
                (
                    SELECT real_uri FROM 'references'
                        WHERE type='artist' AND provider='musicbrainz'
                )
                AND real_uri NOT IN (SELECT real_uri from '_untagged')
                AND real_uri NOT IN (SELECT real_uri from '_incompletes')
            """
        )




class Mapper:
    """ [ Map Spotify item to Musicbrainz ]

        Steps:
        - Read a spotify item's info
        - Check if related local mbz info exists
        - Request Musicbrainz API for the info
        - Save the best match to Database
    """

    @classmethod
    def map_all(cls):
        uris = cls.find_unmapped()
        print( '[UNMAPPED] {} TRACKS.'.format(len(uris)) )
        for i,uri in enumerate(uris):
            print( i+1 )
            cls.toMbz( uri )

    @classmethod
    def find_unmapped(cls):
        print( '[find_unmapped()] TO BE IMPLEMENTED' )
        return []

    @classmethod
    def get_pair_refs(cls, uri):
        # print('[FUNC]__get_references__', uri)

        spt = Reference.get(uri)
        mbz = session.query(Reference).filter(
            Reference.real_uri == spt.real_uri,
            Reference.provider == 'musicbrainz'
        ).first()
        print( '[FUNC]__get_pair_refs__:', spt, mbz )

        return (spt, mbz)

    @classmethod
    def toMbz(cls, uri):
        """
            Params:
            - uri [type:String]: spotify item's uri

            Return: <Reference> of MBZ item
        """
        # Check track's references [Spotify] & [Musicbrainz]
        spt,mbz = cls.get_pair_refs( uri )

        if not spt:
            print( '[SKIP] SPT DOES NOT EXIST.', spt )
            sleep(3)
        elif spt and mbz:
            print( '[SKIP] TAG EXISTS.', mbz )
        elif spt and not mbz:
            # Retrive essential Query fields
            info = cls.get_spotify_info( uri )
            print( info, spt )
            if not info:
                print( '[SKIP] SPT MARKED AS INCOMPLETE.', info )
                session.merge( Incomplete(spt.real_uri) )
                session.commit()
            else:
                mbz = cls.get_musicbrainz_info(info)

        return mbz


    @classmethod
    def get_spotify_info(cls, uri):
        print( '[get_spotify_info()] TO BE IMPLEMENTED' )
        return None

    @classmethod
    def tagging(cls, real_uri, **query):
        print( '[tagging()] TO BE IMPLEMENTED' )
        return None



class MapTrack(Mapper):
    """ [ Map a Spotify track to Musicbrainz ]
    """

    @classmethod
    def find_unmapped(cls):
        return UnMapped.find_unmapped_tracks()

    @classmethod
    def get_spotify_info(cls, track_uri):
        """ [ Base on track_uri, return names of track/album/artist ]
        """
        print('[FUNC]__get_spt_info__:{}'.format(track_uri))
        tsql = text(
            """
            SELECT t.uri, a.uri, r.uri FROM
                "spotify_Tracks" AS t,
                "spotify_Albums" AS a,
                "spotify_Artists" AS r
            INNER JOIN includes AS ta
                ON t.uri=ta.child_uri AND a.uri=ta.parent_uri
            INNER JOIN includes AS tr
                ON t.uri=tr.child_uri AND r.uri=tr.parent_uri
            WHERE t.uri = :t_uri
            """
        )
        with engine.connect() as con:
            info = con.execute(tsql, t_uri=track_uri).fetchone()
            t,a,r = info if info else (None,None,None)
            track = SpotifyTrack.get( t )
            album = SpotifyAlbum.get( a )
            artist = SpotifyArtist.get( r )

        return (track,album,artist) if track and album and artist else None

    @classmethod
    def tagging(cls, info):
        print('[FUNC]__tagging__', info)
        track, album, artist = info
        jsondata = MbzAPI.best_match_track(
            name=track.name, release=album.name, artist=artist.name,
        )
        if not jsondata:
            print('[SKIP] NO TAG FOUND. MARKED AS UNTAGGED.', jsondata)
            session.merge( UnTagged(spt.real_uri) )
            session.commit()
        else:
            print( '\t[HIT]', jsondata.get('title') )
            mbz =  MbzOpsTrack.load( jsondata, spt.real_uri )

        return mbz




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
        print('[FUNC]__get_spotify_album_info__')
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
        print('[FUNC]__tagging__')
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
        print('[FUNC]__get_spotify_artist_info__')
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
        print('[FUNC]__tagging__')
        jsondata = MbzAPI.best_match_artist(
            name=artist.name
        )
        print( jsondata )
        mbz = MusicbrainzArtist.load( jsondata, real_uri )
        return mbz




print('[  OK  ] __IMPORTED__: {}'.format(__name__))

