"=============================================================================
" FILE: custom.vim
" AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#custom#_get() abort
  if !exists('s:custom')
    call deoppet#custom#_init()
  endif

  return s:custom
endfunction

function! deoppet#custom#_init() abort
  let s:custom = {}
  let s:custom.option = deoppet#init#_options()
endfunction

function! deoppet#custom#option(name_or_dict, ...) abort
  let custom = deoppet#custom#_get().option

  call s:set_custom(custom, a:name_or_dict, get(a:000, 0, ''))
endfunction

function! s:set_custom(dest, name_or_dict, value) abort
  if type(a:name_or_dict) == v:t_dict
    call extend(a:dest, a:name_or_dict)
  else
    let a:dest[a:name_or_dict] = a:value
  endif
endfunction
