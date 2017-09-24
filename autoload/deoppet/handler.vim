"=============================================================================
" FILE: handler.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#handler#_init() abort
  augroup deoppet
    autocmd!
    autocmd BufWritePost * call _deoppet_event('BufWritePost')
  augroup END
endfunction
