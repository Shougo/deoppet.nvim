"=============================================================================
" FILE: init.vim
" AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
" License: MIT license
"=============================================================================

function! deoppet#init#_initialize() abort
  if exists('g:deoppet#_channel_id')
    return
  endif

  call deoppet#init#_channel()

  let g:deoppet#_target_text = ''

  augroup deoppet
    autocmd!
  augroup END

  call _deoppet_event('FileType')
endfunction
function! deoppet#init#_channel() abort
  if !has('python3')
    call deoppet#util#print_error(
          \ 'deoppet requires Python3 support("+python3").')
    return v:true
  endif
  if !has('nvim-0.5.0')
    call deoppet#util#print_error('deoppet requires nvim 0.5.0+.')
    return v:true
  endif

  try
    if deoppet#util#has_yarp()
      let g:deoppet#_yarp = yarp#py3('deoppet')
      call g:deoppet#_yarp.request('_deoppet_init')
      let g:deoppet#_channel_id = 1
    else
      " rplugin.vim may not be loaded on VimEnter
      if !exists('g:loaded_remote_plugins')
        runtime! plugin/rplugin.vim
      endif

      call _deoppet_init()
    endif
  catch
    call deoppet#util#print_error(v:exception)
    call deoppet#util#print_error(v:throwpoint)

    let python_version_check = deoppet#init#_python_version_check()
    if python_version_check
      call deoppet#util#print_error(
            \ 'deoppet requires Python 3.6.1+.')
    endif

    if deoppet#util#has_yarp()
      if !has('nvim') && !exists('*neovim_rpc#serveraddr')
        call deoppet#util#print_error(
              \ 'deoppet requires vim-hug-neovim-rpc plugin in Vim.')
      endif

      if !exists('*yarp#py3')
        call deoppet#util#print_error(
              \ 'deoppet requires nvim-yarp plugin.')
      endif
    else
      call deoppet#util#print_error(
          \ 'deoppet failed to load. '
          \ .'Try the :UpdateRemotePlugins command and restart Neovim. '
          \ .'See also :checkhealth.')
    endif

    return v:true
  endtry
endfunction
function! deoppet#init#_check_channel() abort
  return exists('g:deoppet#_channel_id')
endfunction

function! deoppet#init#_python_version_check() abort
  python3 << EOF
import vim
import sys
vim.vars['deoppet#_python_version_check'] = (
    sys.version_info.major,
    sys.version_info.minor,
    sys.version_info.micro) < (3, 6, 1)
EOF
  return g:deoppet#_python_version_check
endfunction
function! deoppet#init#_options() abort
  return {
        \ 'ft_snippets_map': {},
        \ 'snippets': [],
        \ }
endfunction
