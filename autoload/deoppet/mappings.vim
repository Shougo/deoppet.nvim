"=============================================================================
" FILE: mappings.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#mappings#_init() abort
  inoremap <silent><expr> <Plug>(deoppet_expand)
      \ deoppet#mappings#_expand_impl()

  " Test
  imap <C-k>  <Plug>(deoppet_expand)
endfunction

function! deoppet#mappings#_expand_impl() abort
  return s:trigger('_deoppet_mapping')
endfunction

function! s:pre_trigger() abort
  let cur_text = deoppet#util#_get_cur_text()

  let col = col('.')
  let expr = ''
  if mode() !=# 'i'
    " Fix column.
    let col += 2
  endif

  return [cur_text, col, expr]
endfunction

function! s:trigger(function) abort
  let [cur_text, col, expr] = s:pre_trigger()

  let expr .= printf("\<ESC>:call %s(%s,%d)\<CR>",
        \ a:function, string(cur_text), col)

  return expr
endfunction
