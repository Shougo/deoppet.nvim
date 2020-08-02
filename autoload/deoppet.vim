"=============================================================================
" FILE: deoppet.vim
" AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#initialize() abort
  return deoppet#init#_initialize()
endfunction

function! deoppet#expand(trigger) abort
  call deoppet#util#_start_insert()

  call _deoppet_expand(a:trigger)
  return ''
endfunction
