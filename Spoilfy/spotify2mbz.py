#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:



#-> TEST only
if __name__ == '__main__':
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from webapi.spotify import SpotifyAPI
    from webapi.musicbrainz import MusicbrainzAPI
else:
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.webapi.spotify import SpotifyAPI
    from Spoilfy.webapi.musicbrainz import MusicbrainzAPI




class Tagger():
    pass


class TaggerSPT2MBZ():
    pass






print('[  OK  ] __IMPORTED__: {}'.format(__name__))

