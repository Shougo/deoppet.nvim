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

function! deoppet#expandable() abort
  if !exists('b:deoppet_snippets')
    return v:false
  endif

  let cur_text = deoppet#util#_get_cur_text()
  let trigger = deoppet#util#_get_cursor_snippet(
        \ b:deoppet_snippets, cur_text)

  return trigger !=# ''
endfunction
