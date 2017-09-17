let s:suite = themis#suite('toml')
let s:assert = themis#helper('assert')

function! s:suite.dummy() abort
  call s:assert.equals(1, 1)
endfunction
