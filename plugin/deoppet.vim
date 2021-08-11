"=============================================================================
" FILE: deoppet.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

if exists('g:loaded_deoppet')
  finish
endif
let g:loaded_deoppet = 1

let s:name = fnamemodify(expand('<sfile>'), ':t:r')

silent! call ddc#register_source({
      \ 'name': s:name,
      \ 'path': printf('%s/denops/ddc/sources/%s.ts',
      \                fnamemodify(expand('<sfile>'), ':h:h'), s:name),
      \ })
