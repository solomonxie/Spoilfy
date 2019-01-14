#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import uuid

#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
else:
    # Package Import Hint: $ python -m Spoilfy.orm.spotify
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI



# ==============================================================
# >>>>>>>>>>>>>>>[    Operator Classes     ] >>>>>>>>>>>>>>>>>
# ==============================================================


class SptOps:
    pass


class SptOpsAccount(SptOps):
    """ [ Spotify Account Operations ]

    """

    @classmethod
    def get_user_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def load(cls, jsondata):
        # Insert items to DB
        item = cls(jsondata)
        # Add reference
        session.merge( Reference(item) )
        session.commit
        return item



class SptOpsTrack(SptOps):
    """ [ Spotify Track Operations ]

    """

    @classmethod
    def load(cls, jsondata):
        track = session.merge( SpotifyTrack(jsondata) )
        ref = session.merge( Reference(track) )
        cls.include_album( jsondata )
        cls.include_artists( jsondata )
        session.commit()

    @classmethod
    def loads(cls, jsondata):
        return [ cls.load(o) for o in jsondata.get('items',[]) ]

    @classmethod
    def include_album(cls, trackdata):
        t = trackdata.get('track',{})
        child = t.get('uri')
        a = t.get('album', {})
        parent = a.get('uri')
        # Insert album data if not exists
        album = session.query( SpotifyAlbum ).filter(
            SpotifyAlbum.uri == parent
        ).first()

        if not album:
            SpotifyAlbum.load( {'album': a} )
            session.commit()
        else:
            print( '\t[  JUMPED  ] Already has {}'.format(parent) )

        return album

    @classmethod
    def include_artists(cls, trackdata):
        t = trackdata.get('track', {})
        child = t.get('uri')
        refs = []
        for r in t.get('artists', []):
            parent = r.get('uri')
            # Insert album data if not exists
            artist = session.query( SpotifyAlbum ).filter(
                SpotifyArtist.uri == parent
            ).first()
            if not artist:
                inc = session.merge( Include(parent, child) )
                artist = session.merge( SpotifyArtist(r) )
                refs.append( session.merge(Reference(artist)) )
                # print( '\t[APPENDIX ARTIST]', artist.name, artist.uri )
            else:
                print( '\t[  JUMPED  ] Already has {}'.format(parent) )
        # Submit changes
        session.commit()
        if refs:
            print( '\t[  APPENDIX  ] {}/{} [ARTISTS].'.format(
                len(refs), len( t.get('artists', []) )
            ))
        return refs




class SptOpsAlbum(SptOps):
    """ [ Spotify Album Operations ]

    """

    @classmethod
    def load(cls, jsondata):
        album = session.merge( cls(jsondata) )
        ref = session.merge( Reference(album) )
        cls.include_tracks( jsondata )
        cls.include_artists( jsondata )
        session.commit()

    @classmethod
    def loads(cls, jsondata):
        return [ cls.load(o) for o in jsondata.get('items',[]) ]

    @classmethod
    def include_tracks(cls, albumdata):
        refs = []
        album = albumdata.get('album', {})
        artists = album.get('artists',[])
        parent = album.get('uri')
        for t in album.get('tracks',{}).get('items',[]):
            child = t.get('uri')
            track = session.query( SpotifyTrack ).filter(
                SpotifyTrack.uri == child
            ).first()
            # Insert track data if not exists
            if not track:
                d = {'track':t, 'album':album, 'artists':artists}
                inc = session.merge( Include(parent, child) )
                track = session.merge( SpotifyTrack(d) )
                refs.append( session.merge(Reference(track)) )
                SpotifyTrack.include_album( d )
                SpotifyTrack.include_artists( d )
                # print( '\t[APPENDIX TRACK]', track.name, track.uri )
            else:
                print( '\t[  JUMPED  ] Already has {}'.format(child) )
        # Submit changes
        session.commit()
        if refs:
            print( '\t[  APPENDIX  ] {}/{} [TRACKS].'.format(
                len( refs ), len( album.get('tracks',{}).get('items',[]) )
            ))
        return refs

    @classmethod
    def include_artists(cls, albumdata):
        album = albumdata.get('album', {})
        child = album.get('uri')
        refs = []
        artists = album.get('artists',[])
        for r in artists:
            parent = r.get('uri')
            artist = session.query( SpotifyArtist ).filter(
                SpotifyArtist.uri == r.get('uri')
            ).first()
            # Insert artist data if not exists
            if not artist:
                inc = session.merge( Include(parent, child) )
                artist = session.merge( SpotifyArtist(r) )
                refs.append( session.merge(Reference(artist)) )
                # print( '\t[APPENDIX ARTIST]', artist.name, artist.uri )
            else:
                print( '\t[  JUMPED  ] Already has {}'.format(parent) )
        # Submit changes
        session.commit()
        if refs:
            print( '\t[  APPENDIX  ] {}/{} [ARTISTS].'.format(
                len(refs), len(artists)
            ))
        return refs



class SptOpsArtist(SptOps):
    """ [ Spotify Artist Operations ]

    """

    @classmethod
    def loads(cls, jsondata):
        # Insert items to DB
        items = SpotifyArtist.add_resources(jsondata['artists']['items'])
        # Add reference
        refs = Reference.add_resources(items)
        return refs




class SptOpsPlaylist(SptOps):
    """ [ Spotify Playlist Operations ]

    """

    @classmethod
    def loads(cls, jsondata):
        # Insert items to DB
        items = SpotifyPlaylist.add_resources(jsondata['items'])
        # Add reference
        refs = Reference.add_resources(items)
        return refs

    def __add_tracks(self, jsondata):
        return str(jsondata)

    @classmethod
    def add_resources(cls, items):
        """[ Add Resources ]
        :param session: sqlalchemy SESSION binded to DB.
        :param LIST items: must be iteratable.
        :return: inserted resource objects.
        """
        all = []
        for item in items:
            playlist = cls( cls.get_playlist_tracks(item) )
            session.merge( playlist )
            all.append( playlist )

        session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all), cls.__tablename__
        ))

        return all

    @classmethod
    def get_playlist_tracks(cls, item):
        """ [ Get sub item's data through Web API  ]
            This should retrive WebAPI accordingly
            This is to impelemented by children class.
        """
        return item


