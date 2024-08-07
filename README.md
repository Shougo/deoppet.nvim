# deoppet.nvim

**Note**: Active developement on denippet.nvim has stopped. The only future
changes will be bug fixes.

Please see [Denippet.vim](https://github.com/uga-rosa/denippet.vim)


Please read [help](doc/deoppet.txt) for details.

Deoppet is the abbreviation of "dark powered neo-snippet". It provides the
snippet expansion.

## Installation

**Note:** deoppet requires Neovim(0.5.0+) with Python3. See
[requirements](#requirements) if you aren't sure whether you have this.

1. Extract the files and put them in your Neovim directory (usually
   `$XDG_CONFIG_HOME/nvim/`).
2. Execute the `:UpdateRemotePlugins` and restart Neovim.

Note: deoppet does not work in Vim8 environment.

For vim-plug

```viml
Plug 'Shougo/deoppet.nvim', { 'do': ':UpdateRemotePlugins' }
```

For dein.vim

```viml
call dein#add('Shougo/deoppet.nvim')
```

## Requirements

deoppet requires Neovim with if\_python3. If `:echo has("python3")` returns `1`,
then you're done; otherwise, see below.

You can enable Python3 interface with pip:

    pip3 install --user pynvim

If you want to read the pynvim/python3 interface install documentation, you
should read `:help provider-python` and the Wiki.

## Note: Python3 must be enabled before updating remote plugins

If Deoppet was installed prior to Python support being added to Neovim,
`:UpdateRemotePlugins` should be executed manually.

## Screenshots

## Configuration Examples

```vim
call deoppet#initialize()
call deoppet#custom#option('snippets',
\ map(globpath(&runtimepath, 'neosnippets', 1, 1),
\     { _, val -> { 'path': val } }))

imap <C-k>  <Plug>(deoppet_expand)
imap <C-f>  <Plug>(deoppet_jump_forward)
imap <C-b>  <Plug>(deoppet_jump_backward)
smap <C-f>  <Plug>(deoppet_jump_forward)
smap <C-b>  <Plug>(deoppet_jump_backward)

" Use deoppet source.
call ddc#custom#patch_global('sources', ['deoppet'])

" Change source options
call ddc#custom#patch_global('sourceOptions', {
      \ 'deoppet': {'dup': v:true, 'mark': 'dp'},
      \ })
```
