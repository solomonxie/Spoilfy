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
    from orm.common import *
    from orm.user import *
    from orm.spotify import *
    from orm.musicbrainz import *
    from webapi.apiSpotify import *
    from webapi.apiMusicbrainz import *
else:
    # Package Import Hint: $ python -m Spoilfy.sptOps
    from Spoilfy.orm.common import *
    from Spoilfy.orm.user import *
    from Spoilfy.orm.spotify import *
    from Spoilfy.orm.musicbrainz import *
    from Spoilfy.webapi.apiSpotify import *
    from Spoilfy.webapi.apiMusicbrainz import *



# ==============================================================
# >>>>>>>>>>>>>>>[    Operator Classes     ] >>>>>>>>>>>>>>>>>
# ==============================================================


class SptOps:

    API = None
    ORM = None
    SESSION = None
    ENGINE = None

    def __init__(self, session=None, api=None):
        with open('./webapi/.spotify_app.json', 'r') as f:
            self.API = SpotifyAPI( json.loads(f.read()) ) if not api else api
        if session:
            self.SESSION = session




class SptOpsAccount(SptOps):
    """ [ Spotify Account Operations ]

    """
    ORM = SpotifyAccount

    def get_user_by_name(self, name):
        return self.ORM.query.filter(self.ORM.name == name).first()

    def get_user_by_id(self, id):
        return self.ORM.query.filter(self.ORM.id == id).first()

    def get_my_profile(self):
        return SptOpsAccount.load( self.API.get_my_profile() )

    def load(self, jsondata):
        # Insert items to DB
        user = self.SESSION.merge( self.ORM(jsondata) )
        # Add reference
        self.SESSION.merge( Reference(user) )
        self.SESSION.commit()
        return user



class SptOpsTrack(SptOps):
    """ [ Spotify Track Operations ]

    """
    ORM = SpotifyTrack

    def retrive_my_tracks(self):
        """
            TODO:
            - Async retrive multiple pages from API
        """
        print( '\n[  OPS  ] SptOpsTrack' )
        for page in SptOpsTrack.API.get_my_tracks():
            SptOpsTrack.loads( page )

    def loads(self, jsondata):
        all = []
        for o in jsondata.get('items', []):
            all.append( self.load(o) )

    def load(self, jsondata):
        track = self.SESSION.merge( self.ORM(jsondata) )
        ref = self.SESSION.merge( Reference(track) )
        self.SESSION.commit()
        return ref




class SptOpsAlbum(SptOps):
    """ [ Spotify Album Operations ]

    """
    ORM = SpotifyAlbum

    def retrive_my_albums(self):
        """
            TODO:
            - Async retrive multiple pages from API
        """
        print( '\n[  OPS  ] SptOpsAlbum' )
        for page in SptOpsAlbum.API.get_my_albums():
            albums = SptOpsAlbum.loads( page )
            # print( '[  OK  ] Inserted {} User albums.'.format(len(albums)) )

    def loads(self, jsondata):
        for o in jsondata.get('items', []):
            ref = self.load(o)
            print( '[NEW]', ref )

    def load(self, jsondata):
        album = self.SESSION.merge( self.ORM(jsondata) )
        ref = self.SESSION.merge( Reference(album) )
        self.SESSION.commit()
        return ref




class SptOpsArtist(SptOps):
    """ [ Spotify Artist Operations ]

    """
    ORM = SpotifyArtist

    def retrive_my_artists(self):
        print( '\n[  OPS  ] SptOpsArtist' )
        for page in SptOpsArtist.API.get_my_artists():
            artists = SptOpsArtist.loads( page )
            # print( '[  OK  ] Inserted {} User artists.'.format(len(artists)) )

    def load(self, jsondata):
        album = self.SESSION.merge( self.ORM(jsondata) )
        ref = self.SESSION.merge( Reference(album) )
        self.SESSION.commit()
        return ref

    def loads(self, jsondata):
        return [self.load(o) for o in jsondata.get('artists',{}).get('items',[])]




class SptOpsPlaylist(SptOps):
    """ [ Spotify Playlist Operations ]

    """
    ORM = SpotifyPlaylist

    def retrive_my_playlists(self):
        """
            TODO:
            - Async retrive multiple pages from API
        """
        print( '\n[  OPS  ] SptOpsPlaylist' )
        for page in SptOpsPlaylist.API.get_my_playlists():
            playlists = SptOpsPlaylist.loads( page )
            # print('[  OK  ] Inserted {} User playlists'.format(len(playlists)))

    def loads(self, jsondata):
        for o in jsondata.get('items', []):
            ref = self.load( o )

    def load(self, jsondata):
        playlist = self.SESSION.merge( self.ORM(jsondata) )
        ref = self.SESSION.merge( Reference(playlist) )
        self.SESSION.commit()
        return ref





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

    def _find_missing(self, sql):
        with self.ENGINE.connect() as con:
            records = con.execute(sql)
            uris = [ u for u, in records ]
        return uris

    def find_missing_tracks(self):
        return self._find_missing( self.SQL_MISSING_TRACKS )
    def find_missing_albums(self):
        return self._find_missing( self.SQL_MISSING_ALBUMS )
    def find_missing_artists(self):
        return self._find_missing( self.SQL_MISSING_ARTISTS )

    #---------------------------------------------------------#

    def fix_missing_tracks(self):
        refs = []
        missings = self.find_missing_tracks()
        print( '[ FIX ] {} missing TRACKS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            t = self.API.get_a_track( uri.split(':')[2] )
            if t:
                track = self.SESSION.merge(SpotifyTrack( {'track':t} ))
                refs.append( self.SESSION.merge(Reference( track )) )
                self.SESSION.commit()

        print('\t[ GET ] {}/{} Missing track.'.format(len(refs),len(missings)))

        return refs

    def fix_missing_albums(self):
        refs = []
        missings = self.find_missing_albums()
        print( '[ FIX ] {} missing ALBUMS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            albumdata = {'album': self.API.get_a_album( uri.split(':')[2] )}
            album = self.SESSION.merge(SpotifyAlbum( albumdata ))
            refs.append( self.SESSION.merge(Reference( album )) )
            self.SESSION.commit()

        print('\t[ GET ] {}/{} albums.'.format(len(refs),len(missings)))

        return refs

    def fix_missing_artists(self):
        refs = []
        missings = self.find_missing_artists()
        print( '[ FIX ] {} missing ARTISTS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            artistdata = self.API.get_a_artist( uri.split(':')[2] )
            artist = self.SESSION.merge(SpotifyArtist( artistdata ))
            refs.append( self.SESSION.merge(Reference( artist )) )
            self.SESSION.commit()

        print('\t[ GET ]{}/{} artists.'.format(len(refs),len(missings)))

        return refs



class SptOpsInclude(SptOps):
    """ [ Bind related sub-items ]
    """

    SQL_TRACK_ALBUMS = """
        SELECT uri from spotify_Tracks
            WHERE uri NOT IN ( SELECT child_uri FROM includes
                WHERE parent_type = 'album')
    """

    SQL_TRACK_ARTISTS = """
        SELECT uri from spotify_Tracks
            WHERE uri NOT IN ( SELECT child_uri FROM includes
                WHERE parent_type = 'artist')
    """

    SQL_ALBUM_TRACKS = """
        SELECT uri from spotify_Albums
            WHERE uri NOT IN ( SELECT parent_uri FROM includes
                WHERE child_type = 'track')
    """

    SQL_ALBUM_ARTISTS = """
        SELECT uri from spotify_Albums
            WHERE uri NOT IN ( SELECT child_uri FROM includes
                WHERE parent_type = 'artist')
    """

    SQL_PLAYLIST_TRACKS = """
        SELECT uri from spotify_Playlists
            WHERE uri NOT IN ( SELECT parent_uri FROM includes
                WHERE child_type = 'track')
    """

    def find_unbinded(self, sql):
        with self.ENGINE.connect() as con:
            records = con.execute(sql)
            uris = [ u for u, in records ]
        return uris

    def track_bindings(self):
        # Unbinded Tracks' albums
        unbinded = self.find_unbinded(self.SQL_TRACK_ALBUMS)
        print('[UNBINDED]', len(unbinded))
        for uri in unbinded:
            data = json.loads( SpotifyTrack.get(uri).albumdata )
            self.load_album_of_track(uri, data)
        # Unbinded Tracks' artists
        unbinded = self.find_unbinded(self.SQL_TRACK_ARTISTS)
        print('[UNBINDED]', len(unbinded))
        for uri in unbinded:
            data = json.loads( SpotifyTrack.get(uri).artistdata )
            self.load_artists_of_track(uri, data)

    def album_bindings(self):
        self.load_tracks_of_album()
        self.load_artists_of_album()

    def playlist_bindings(self):
        self.load_tracks_of_playlist()


    #---------------------------------------------------------#

    def load_album_of_track(self, child, albumdata):
        parent = albumdata.get('uri')
        inc = self.SESSION.merge( Include(parent, child) )
        print( '\t[BIND]', inc )
        self.SESSION.commit()

        return inc

    def load_artists_of_track(self, child, artistdata):
        incs = []
        for r in artistdata:
            parent = r.get('uri')
            inc = self.SESSION.merge(Include(parent, child))
            incs.append( inc )
            print( '\t[BIND]', inc )
        self.SESSION.commit()

        return incs

    def load_tracks_of_album(self, parent, tracksdata):
        incs = []
        for t in tracksdata.get('items', []):
            child = t.get('uri')
            if child:
                # Bind tracks to album
                inc = self.SESSION.merge( Include(parent, child) )
                incs.append( inc )
                print( '\t[BIND]', inc )
                # -> Also bind artists to each track
                SptOpsTrack.include_artists( t )
        self.SESSION.commit()

        return incs

    def load_artists_of_album(self, albumdata):
        child = albumdata.get('uri')

        incs = []
        for r in albumdata.get('artists', []):
            parent = r.get('uri')
            inc = self.SESSION.merge( Include(parent, child) )
            incs.append( inc )
            print( '\t[BIND]', inc )
        self.SESSION.commit()

        return incs

    def load_tracks_of_playlist(self, parent, tracksdata):
        for o in tracksdata.get('items',[]):
            child = o.get('track',{}).get('uri')
            if child:
                inc = self.SESSION.merge( Include(parent, child) )
                self.SESSION.commit()

    #-------------------------------------------------------#

    def playlist_includes(self, playlistdata):
        # Bind tracks to an album [Loop pages]
        id = playlistdata.get('id')
        parent = 'spotify:playlist:{}'.format(id)
        # original playlist uri: "spotify:user:xxxxxxxx:playlist:xxxxxxx"
        for page in self.API.get_playlist_tracks( id ):
            self.include_tracks( parent, page )

    def album_includes(self, albumdata):
        # Bind artists to an album
        self.include_artists( albumdata )

        # Bind tracks to an album [Loop pages]
        id = albumdata.get('id')
        parent = albumdata.get('uri')
        for page in self.API.get_album_tracks( id ):
            self.include_tracks( parent, page )


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

    #====> Insert data

    # =ACCOUNT=
    # print( '\n[  OPS  ] SptOpsAccount' )
    # me = SptOpsAccount.get_my_profile()
    # print( '\t Me:', me.name )

    # SptOpsTrack.retrive_my_tracks()
    # SptOpsAlbum.retrive_my_albums()
    # SptOpsArtist.retrive_my_artists()
    # SptOpsPlaylist.retrive_my_playlists()

    #====> Bind includes
    # SptOpsInclude.track_bindings()


    #====> Find missings
    # tracks = SptOpsMissing.find_missing_tracks()
    # print( '[MISSING]', len(tracks) )
    # albums = SptOpsMissing.find_missing_albums()
    # print( '[MISSING]', len(albums) )
    # artists = SptOpsMissing.find_missing_artists()
    # print( '[MISSING]', len(artists) )

    # Complete missings
    # refs = SptOpsMissing.fix_missing_tracks()
    # refs = SptOpsMissing.fix_missing_albums()
    # refs = SptOpsMissing.fix_missing_artists()
