let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Workspace/repos/Spoilfy/Spoilfy
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py
badd +17 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_spotify.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py
badd +3 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_common.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py
badd +4 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiMusicbrainz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/user.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_user.py
badd +1 /private/tmp/abc.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiSpotify.py
badd +32 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiSpotify.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/sptOps.py
badd +121 ~/Workspace/repos/Spoilfy/Spoilfy/test_sptOps.py
badd +39 ~/Workspace/repos/Spoilfy/Spoilfy/test_spotify2mbz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/mbzOps.py
badd +42 ~/Workspace/repos/Spoilfy/Spoilfy/test_mbzOps.py
badd +1 ~/dotfiles/vim/vimrc
badd +1 ~/dotfiles/vim/vimrc-keymappings
badd +1 ~/dotfiles/vim/vimrc-plugins
badd +1 ~/dotfiles/vim/vimrc-ui
badd +263 ~/Workspace/repos/Spoilfy/draft/sqlschemas/ORM2/CREATE_GRP_SPOTIFY.py
badd +159 ~/Workspace/repos/Spoilfy/draft/sqlschemas/ORM2/COMMONS.py
badd +114 ~/Workspace/repos/Spoilfy/draft/sqlschemas/ORM2/CREATE_GRP_USER.py
badd +1 ~/Workspace/repos/Spoilfy/draft/sqlschemas/ORM2/users.json
badd +148 ~/Workspace/repos/Spoilfy/draft/sqlschemas/ORM/CREATE_ALBUMS.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_musicbrainz.py
argglobal
silent! argdel *
$argadd ~/dotfiles/vim/vimrc
$argadd ~/dotfiles/vim/vimrc-keymappings
$argadd ~/dotfiles/vim/vimrc-plugins
$argadd ~/dotfiles/vim/vimrc-ui
edit ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 55 - ((39 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
55
normal! 0
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/test_spotify2mbz.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/test_spotify2mbz.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/test_spotify2mbz.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=1
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 61 - ((39 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
61
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/sptOps.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/sptOps.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/sptOps.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/sptOps.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 45 - ((2 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
45
normal! 024|
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/test_sptOps.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/test_sptOps.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/test_sptOps.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 137 - ((31 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
137
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiSpotify.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiSpotify.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiSpotify.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiSpotify.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 21 - ((20 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
21
normal! 0
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiSpotify.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiSpotify.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiSpotify.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 33 - ((26 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
33
normal! 012|
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 47 - ((6 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
47
normal! 037|
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiMusicbrainz.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiMusicbrainz.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiMusicbrainz.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 10 - ((9 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10
normal! 042|
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 212 - ((34 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
212
normal! 08|
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/test_common.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_common.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_common.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 31 - ((24 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 227 - ((19 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
227
normal! 0
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/test_spotify.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_spotify.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_spotify.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 170 - ((25 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
170
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 153 - ((19 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
153
normal! 0
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/test_musicbrainz.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_musicbrainz.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_musicbrainz.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 45 - ((38 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
45
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/mbzOps.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/mbzOps.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/mbzOps.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/mbzOps.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 162 - ((39 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
162
normal! 0
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/test_mbzOps.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/test_mbzOps.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/test_mbzOps.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=1
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 40 - ((39 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
40
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/orm/user.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/user.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/user.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/user.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 113 - ((38 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
113
normal! 010|
wincmd w
argglobal
if bufexists('~/Workspace/repos/Spoilfy/Spoilfy/orm/test_user.py') | buffer ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_user.py | else | edit ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_user.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 38 - ((37 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
38
normal! 012|
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
tabnext 2
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToOF
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
