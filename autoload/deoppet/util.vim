"=============================================================================
" FILE: util.vim
" AUTHOR:  Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

let s:is_windows = has('win32') || has('win64')
let s:is_mac = !s:is_windows && !has('win32unix')
      \ && (has('mac') || has('macunix') || has('gui_macvim') ||
      \   (!isdirectory('/proc') && executable('sw_vers')))

function! deoppet#util#print_error(string) abort
  echohl Error | echomsg '[deoppet] '
        \ . deoppet#util#string(a:string) | echohl None
endfunction
function! deoppet#util#print_warning(string) abort
  echohl WarningMsg | echomsg '[deoppet] '
        \ . deoppet#util#string(a:string) | echohl None
endfunction
function! deoppet#util#print_debug(string) abort
  echomsg '[deoppet] ' . deoppet#util#string(a:string)
endfunction
function! deoppet#util#print_message(string) abort
  echo '[deoppet] ' . deoppet#util#string(a:string)
endfunction
function! deoppet#util#is_windows() abort
  return s:is_windows
endfunction

function! deoppet#util#convert2list(expr) abort
  return type(a:expr) ==# type([]) ? a:expr : [a:expr]
endfunction
function! deoppet#util#string(expr) abort
  return type(a:expr) ==# type('') ? a:expr : string(a:expr)
endfunction

function! deoppet#util#has_yarp() abort
  return !has('nvim') || get(g:, 'deoppet#enable_yarp', 0)
endfunction

function! deoppet#util#_get_cur_text() abort
  return
        \ (mode() ==# 'i' ? (col('.')-1) : col('.')) >= len(getline('.')) ?
        \      getline('.') :
        \      matchstr(getline('.'),
        \         '^.*\%' . col('.') . 'c' . (mode() ==# 'i' ? '' : '.'))
endfunction
function! deoppet#util#_get_next_text() abort
  return getline('.')[len(deoppet#util#_get_cur_text()) :]
endfunction

function! deoppet#util#_get_cursor_snippet(snippets, cur_text) abort
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
endfunction

function! deoppet#util#_select_text(text) abort
  let len = len(a:text) - 1
  if &l:selection ==# 'exclusive'
    let len += 1
  endif

  let mode = mode()

  " Insert the text
  call deoppet#util#_insert_text(a:text)
  execute 'normal!' len . 'h'

  " Select the text
  normal! v
  call cursor(0, col('.') + (mode ==# 'i' ? len + 1 : len))
  execute 'normal! ' "\<C-g>"
endfunction
function! deoppet#util#_insert_text(text) abort
  " Insert the text
  execute 'normal!' ((col('.') == col('$') ? 'A' : 'i') . a:text)
  stopinsert
endfunction
function! deoppet#util#_select_pos(pos) abort
  " Select to the pos
  normal! v
  call cursor(0, a:pos[1] + 1)
  execute 'normal! ' "\<C-g>"
endfunction
function! deoppet#util#_start_insert() abort
  if mode() ==# 'i'
    return
  endif

  if col('.') == col('$')
    startinsert!
  else
    startinsert
  endif
endfunction

function! deoppet#util#_indent_snippet(begin, end) abort
  if a:begin > a:end
    return
  endif

  let pos = getpos('.')

  let equalprg = &l:equalprg
  try
    setlocal equalprg=

    for line_nr in range(a:begin, a:end)
      call cursor(line_nr, 0)

      silent normal! ==
    endfor
  finally
    let &l:equalprg = equalprg
    call setpos('.', pos)
  endtry
endfunction
