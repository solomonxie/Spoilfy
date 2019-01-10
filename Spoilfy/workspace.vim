let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Workspace/repos/Spoilfy/Spoilfy
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +106 ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py
badd +63 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_spotify.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/musicbrainz.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_musicbrainz.py
badd +17 ~/Workspace/repos/Spoilfy/Spoilfy/orm/common.py
badd +3 ~/Workspace/repos/Spoilfy/Spoilfy/orm/test_common.py
badd +1 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/apiMusicbrainz.py
badd +4 ~/Workspace/repos/Spoilfy/Spoilfy/webapi/test_apiMusicbrainz.py
argglobal
silent! argdel *
$argadd spotify2mbz.py
edit ~/Workspace/repos/Spoilfy/Spoilfy/spotify2mbz.py
set splitbelow splitright
set nosplitbelow
wincmd t
set winminheight=1 winminwidth=1 winheight=1 winwidth=1
argglobal
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 90 - ((9 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
90
normal! 08|
tabedit ~/Workspace/repos/Spoilfy/Spoilfy/orm/spotify.py
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
let s:l = 220 - ((26 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
220
normal! 053|
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
let s:l = 66 - ((21 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
66
normal! 015|
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
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
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=1
setlocal fen
let s:l = 156 - ((35 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
156
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
let s:l = 38 - ((28 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
38
normal! 022|
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
let s:l = 29 - ((22 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
29
normal! 05|
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
let s:l = 29 - ((22 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
29
normal! 014|
wincmd w
exe 'vert 1resize ' . ((&columns * 84 + 85) / 170)
exe 'vert 2resize ' . ((&columns * 85 + 85) / 170)
tabnext 1
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
