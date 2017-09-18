"=============================================================================
" FILE: util.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#util#_get_cur_text() abort
  return
        \ (mode() ==# 'i' ? (col('.')-1) : col('.')) >= len(getline('.')) ?
        \      getline('.') :
        \      matchstr(getline('.'),
        \         '^.*\%' . col('.') . 'c' . (mode() ==# 'i' ? '' : '.'))
endfunction
function! deoppet#util#_get_next_text() abort "{{{
  return getline('.')[len(deoppet#util#_get_cur_text()) :]
endfunction"}}}

function! deoppet#util#_get_cursor_snippet(snippets, cur_text) abort "{{{
  let cur_word = matchstr(a:cur_text, '\S\+$')
  if cur_word !=# '' && has_key(a:snippets, cur_word)
      return cur_word
  endif

  while cur_word !=# ''
    if has_key(a:snippets, cur_word) &&
          \ get(a:snippets[cur_word].options, 'word', 0)
      return cur_word
    endif

    let cur_word = substitute(cur_word, '^\%(\w\+\|\W\)', '', '')
  endwhile

  return cur_word
endfunction"}}}
