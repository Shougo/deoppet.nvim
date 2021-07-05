"=============================================================================
" FILE: deoppet.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

if exists('g:loaded_ddc_deoppet')
  finish
endif
let g:loaded_ddc_deoppet = 1

silent! call ddc#register_source({
      \ 'name': 'deoppet',
      \ 'path': fnamemodify(expand('<sfile>'), ':h:h:h')
      \         . '/denops/ddc/sources/deoppet.ts',
      \ })
