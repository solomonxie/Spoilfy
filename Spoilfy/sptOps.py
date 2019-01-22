#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json

from sqlalchemy.orm import aliased

#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__', 'sptOps']:
    from sptOps import *
    from orm.common import *
    from orm.user import *
    from orm.spotify import *
    from orm.musicbrainz import *
    from webapi.apiSpotify import *
    from webapi.apiMusicbrainz import *
else:
    # Package Import Hint: $ python -m Spoilfy.sptOps
    from Spoilfy.sptOps import *
    from Spoilfy.orm.common import *
    from Spoilfy.orm.user import *
    from Spoilfy.orm.spotify import *
    from Spoilfy.orm.musicbrainz import *
    from Spoilfy.webapi.apiSpotify import *
    from Spoilfy.webapi.apiMusicbrainz import *



# ==============================================================
# >>>>>>>>>>>>>>>[    Operator Classes     ] >>>>>>>>>>>>>>>>>
# ==============================================================

with open('./webapi/.spotify_app.json', 'r') as f:
    _data = json.loads( f.read() )


class SptOps:

    ORM = None
    SESSION = session
    ENGINE = engine
    # API = SpotifyAPI(_data)




class SptOpsAccount(SptOps):
    """ [ Spotify Account Operations ]

    """
    ORM = SpotifyAccount

    @classmethod
    def get_user_by_name(cls, name):
        return cls.ORM.query.filter(cls.ORM.name == name).first()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.ORM.query.filter(cls.ORM.id == id).first()

    @classmethod
    def get_my_profile(cls):
        return SptOpsAccount.load( cls.API.get_my_profile() )

    @classmethod
    def load(cls, jsondata):
        # Insert items to DB
        user = cls.SESSION.merge( cls.ORM(jsondata) )
        # Add reference
        cls.SESSION.merge( Reference(user) )
        cls.SESSION.commit()
        return user



class SptOpsTrack(SptOps):
    """ [ Spotify Track Operations ]

    """
    ORM = SpotifyTrack

    @classmethod
    def load(cls, jsondata):
        track = cls.SESSION.merge( cls.ORM(jsondata) )
        ref = cls.SESSION.merge( Reference(track) )
        cls.SESSION.commit()
        return ref

    @classmethod
    def loads(cls, jsondata):
        all = []
        for o in jsondata.get('items', []):
            all.append( cls.load(o) )
            print( '[NEW]', ref )
            cls.include_album( o.get('track',{}) )
            cls.include_artists( o.get('track',{}) )
        return all

    #-----------------------------------------#

    @classmethod
    def include_album(cls, trackdata):
        child = trackdata.get('uri', '')
        parent = trackdata.get('album', {}).get('uri', '')
        inc = cls.SESSION.merge( Include(parent, child) )
        print( '\t[BIND]', inc )
        cls.SESSION.commit()

        return inc

    @classmethod
    def include_artists(cls, trackdata):
        child = trackdata.get('uri')

        incs = []
        for r in trackdata.get('artists', []):
            parent = r.get('uri')
            inc = cls.SESSION.merge(Include(parent, child))
            incs.append( inc )
            print( '\t[BIND]', inc )
        cls.SESSION.commit()

        return incs




class SptOpsAlbum(SptOps):
    """ [ Spotify Album Operations ]

    """
    ORM = SpotifyAlbum

    @classmethod
    def loads(cls, jsondata):
        for o in jsondata.get('items', []):
            ref = cls.load(o)
            print( '[NEW]', ref )
            # -> Bind related resources [tracks]/[artists]
            cls.includes( o.get('album', {}) )

    @classmethod
    def includes(cls, albumdata):
        # Bind artists to an album
        cls.include_artists( albumdata )

        # Bind tracks to an album [Loop pages]
        id = albumdata.get('id')
        parent = albumdata.get('uri')
        for page in cls.API.get_album_tracks( id ):
            cls.include_tracks( parent, page )
        # break

    #------------------------------------------#

    @classmethod
    def load(cls, jsondata):
        album = cls.SESSION.merge( cls.ORM(jsondata) )
        ref = cls.SESSION.merge( Reference(album) )
        cls.SESSION.commit()
        return ref


    @classmethod
    def include_tracks(cls, parent, tracksdata):
        incs = []
        for t in tracksdata.get('items', []):
            child = t.get('uri')
            if child:
                # Bind tracks to album
                inc = cls.SESSION.merge( Include(parent, child) )
                incs.append( inc )
                print( '\t[BIND]', inc )
                # -> Also bind artists to each track
                SptOpsTrack.include_artists( t )
        cls.SESSION.commit()

        return incs

    @classmethod
    def include_artists(cls, albumdata):
        child = albumdata.get('uri')

        incs = []
        for r in albumdata.get('artists', []):
            parent = r.get('uri')
            inc = cls.SESSION.merge( Include(parent, child) )
            incs.append( inc )
            print( '\t[BIND]', inc )
        cls.SESSION.commit()

        return incs



class SptOpsArtist(SptOps):
    """ [ Spotify Artist Operations ]

    """
    ORM = SpotifyArtist

    @classmethod
    def load(cls, jsondata):
        album = cls.SESSION.merge( cls.ORM(jsondata) )
        ref = cls.SESSION.merge( Reference(album) )
        cls.SESSION.commit()
        return ref

    @classmethod
    def loads(cls, jsondata):
        return [cls.load(o) for o in jsondata.get('artists',{}).get('items',[])]




class SptOpsPlaylist(SptOps):
    """ [ Spotify Playlist Operations ]

    """
    ORM = SpotifyPlaylist

    @classmethod
    def loads(cls, jsondata):
        for o in jsondata.get('items', []):
            ref = cls.load( o )
            # -> Bind tracks to a playlist
            cls.includes( o )

    @classmethod
    def includes(cls, playlistdata):
        # Bind tracks to an album [Loop pages]
        id = playlistdata.get('id')
        parent = 'spotify:playlist:{}'.format(id)
        # original playlist uri: "spotify:user:xxxxxxxx:playlist:xxxxxxx"
        for page in cls.API.get_playlist_tracks( id ):
            cls.include_tracks( parent, page )
        # break

    #-----------------------------------------------#

    @classmethod
    def load(cls, jsondata):
        playlist = cls.SESSION.merge( cls.ORM(jsondata) )
        ref = cls.SESSION.merge( Reference(playlist) )
        cls.SESSION.commit()
        return ref

    @classmethod
    def include_tracks(cls, parent, tracksdata):
        for o in tracksdata.get('items',[]):
            child = o.get('track',{}).get('uri')
            if child:
                inc = cls.SESSION.merge( Include(parent, child) )
                cls.SESSION.commit()




class SptOpsMissing(SptOps):
    """ [ Search/Fetch for missing data ]
    """

    SQL_MISSING_TRACKS = """
        SELECT child_uri FROM includes
            WHERE child_type='track' AND provider='spotify'
            AND (parent_type='album' OR parent_type='playlist')
            AND child_uri NOT IN (SELECT uri FROM spotify_Tracks)
            GROUP BY child_uri
    """
    SQL_MISSING_ALBUMS = """
        SELECT parent_uri FROM includes
            WHERE parent_type='album' AND provider='spotify'
            AND parent_uri NOT IN (SELECT uri FROM spotify_Albums)
            GROUP BY parent_uri
    """
    SQL_MISSING_ARTISTS = """
        SELECT parent_uri FROM includes
            WHERE parent_type='artist' AND provider='spotify'
            AND parent_uri NOT IN (SELECT uri FROM spotify_Artists)
            GROUP BY parent_uri
    """

    @classmethod
    def _find_missing(cls, sql):
        with cls.ENGINE.connect() as con:
            records = con.execute(sql)
            uris = [ u for u, in records ]
        return uris

    @classmethod
    def find_missing_tracks(cls):
        return cls._find_missing( cls.SQL_MISSING_TRACKS )
    @classmethod
    def find_missing_albums(cls):
        return cls._find_missing( cls.SQL_MISSING_ALBUMS )
    @classmethod
    def find_missing_artists(cls):
        return cls._find_missing( cls.SQL_MISSING_ARTISTS )

    #---------------------------------------------------------#

    @classmethod
    def fix_missing_tracks(cls):
        refs = []
        missings = cls.find_missing_tracks()
        print( '[ FIX ] {} missing TRACKS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            t = cls.API.get_a_track( uri.split(':')[2] )
            if t:
                track = cls.SESSION.merge(SpotifyTrack( {'track':t} ))
                refs.append( cls.SESSION.merge(Reference( track )) )
                cls.SESSION.commit()

        print('\t[ GET ] {}/{} Missing track.'.format(len(refs),len(missings)))

        return refs

    @classmethod
    def fix_missing_albums(cls):
        refs = []
        missings = cls.find_missing_albums()
        print( '[ FIX ] {} missing ALBUMS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            albumdata = {'album': cls.API.get_a_album( uri.split(':')[2] )}
            album = cls.SESSION.merge(SpotifyAlbum( albumdata ))
            refs.append( cls.SESSION.merge(Reference( album )) )
            cls.SESSION.commit()

        print('\t[ GET ] {}/{} albums.'.format(len(refs),len(missings)))

        return refs

    @classmethod
    def fix_missing_artists(cls):
        refs = []
        missings = cls.find_missing_artists()
        print( '[ FIX ] {} missing ARTISTS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            artistdata = cls.API.get_a_artist( uri.split(':')[2] )
            artist = cls.SESSION.merge(SpotifyArtist( artistdata ))
            refs.append( cls.SESSION.merge(Reference( artist )) )
            cls.SESSION.commit()

        print('\t[ GET ]{}/{} artists.'.format(len(refs),len(missings)))

        return refs





# ==============================================================
# >>>>>>>>>>>>>>>>>>[    TEST RUN     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



if __name__ == '__main__':
    try:
        # SpotifyAccount.__table__.drop(engine)
        # SpotifyTrack.__table__.drop(engine)
        # SpotifyAlbum.__table__.drop(engine)
        # SpotifyArtist.__table__.drop(engine)
        # SpotifyPlaylist.__table__.drop(engine)
        # Include.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping SptOps table.')
    finally:
        Base.metadata.create_all(bind=engine)

    #=> Insert data
    # test_SptOpsAccount()
    # test_SptOpsTrack()
    # test_SptOpsAlbum()
    # test_SptOpsArtist()
    # test_SptOpsPlaylist()


    # Complete missings
    # refs = SptOpsMissing.fix_missing_tracks()
    # refs = SptOpsMissing.fix_missing_albums()
    # refs = SptOpsMissing.fix_missing_artists()
