let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Workspace/repos/Spoilfy/Spoilfy
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +241 ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py
badd +19 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_spotify.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_musicbrainz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py
badd +3 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_common.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py
badd +4 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiMusicbrainz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/user.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_user.py
badd +1 /private/tmp/abc.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiSpotify.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiSpotify.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/sptOps.py
badd +0 ~/Workspace/repos/Spoilfy/Spoilfy/test_sptOps.py
argglobal
silent! argdel *
$argadd spotify2mbz.py
edit ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 017|
wincmd w
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
let s:l = 249 - ((25 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
249
normal! 09|
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 93 - ((0 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
93
normal! 042|
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
let s:l = 168 - ((22 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
168
normal! 045|
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
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
argglobal
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 189 - ((19 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
189
normal! 034|
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
let s:l = 73 - ((24 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
73
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 60 - ((17 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
60
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
let s:l = 24 - ((16 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
24
normal! 08|
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 63 - ((30 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
63
normal! 0
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
let s:l = 33 - ((20 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
33
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 19 - ((0 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19
normal! 010|
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
let s:l = 27 - ((14 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
27
normal! 018|
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 42 - ((26 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
42
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
let s:l = 34 - ((24 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
34
normal! 030|
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 9 - ((8 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 85 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 84 + 85) / 170)
tabnext 8
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
