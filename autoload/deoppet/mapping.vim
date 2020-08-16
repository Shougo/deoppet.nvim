"=============================================================================
" FILE: mapping.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#mapping#_init() abort
  inoremap <silent><expr> <Plug>(deoppet_expand)
      \ <SID>trigger('expand')
  inoremap <silent><expr> <Plug>(deoppet_jump_forward)
      \ <SID>trigger('jump_forward')
  inoremap <silent><expr> <Plug>(deoppet_jump_backward)
      \ <SID>trigger('jump_backward')
  snoremap <silent><expr> <Plug>(deoppet_jump_forward)
      \ <SID>trigger('jump_forward')
  snoremap <silent><expr> <Plug>(deoppet_jump_backward)
      \ <SID>trigger('jump_backward')
  xnoremap <silent> <Plug>(deoppet_select_text)
      \ :call <SID>select_text()<CR>
  xnoremap <silent> <Plug>(deoppet_cut_text)
      \ :call <SID>cut_text()<CR>
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

  let expr .= printf("\<ESC>:call %s(%s)\<CR>",
        \ '_deoppet_mapping', string(a:function))

  return expr
endfunction

function! s:select_text() abort
  let g:deoppet#_target_text = substitute(deoppet#util#_get_selected_text(
        \ visualmode(), 1), '\n$', '', '')
endfunction
function! s:cut_text() abort
  let g:deoppet#_target_text = substitute(deoppet#util#_delete_selected_text(
        \ visualmode(), 1), '\n$', '', '')
endfunction
