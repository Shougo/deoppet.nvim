"=============================================================================
" FILE: handler.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#handler#_init() abort
  augroup deoppet
    autocmd!
    autocmd BufWritePost *
          \ silent! call _deoppet_event('BufWritePost')
    autocmd BufNewFile,BufRead,FileType *
          \ silent! call _deoppet_event('FileType')
  augroup END
endfunction
