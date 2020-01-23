# ============================================================================
# FILE: mapping.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import typing

from deoppet.util import debug

from pynvim import Nvim


class Mapping():

    def __init__(self, vim: Nvim) -> None:
        self._vim = vim
        self.clear()

    def debug(self, expr: typing.Any) -> None:
        return debug(self._vim, expr)

    def clear(self) -> None:
        self._ns = self._vim.call('nvim_create_namespace', 'deoppet')
        bvars = self._vim.current.buffer.vars
        if 'deoppet_marks' not in bvars:
            return

        for mark in bvars['deoppet_marks']:
            self._vim.call('nvim_buf_del_extmark', 0, self._ns, mark)

        bvars['deoppet_marks'] = []

    def mapping(self, name: str) -> None:
        bvars = self._vim.current.buffer.vars
        if 'deoppet_marks' not in bvars:
            bvars['deoppet_marks'] = []
        if 'deoppet_snippets' not in bvars:
            return

        if name == 'clear':
            return self.clear()
        if name == 'expand':
            return self.expand()
        if name == 'jump_forward':
            return self.jump(True)
        if name == 'jump_backward':
            return self.jump(False)
        return

    def expand(self) -> None:
        bvars = self._vim.current.buffer.vars
        snippets = bvars['deoppet_snippets']
        cur_text = self._vim.call('deoppet#util#_get_cur_text')
        trigger = self._vim.call('deoppet#util#_get_cursor_snippet',
                                 snippets, cur_text)
        # debug(self._vim, trigger)
        if not trigger:
            return

        # Expand trigger
        cursor = self._vim.current.window.cursor
        linenr = cursor[0]
        buf = self._vim.current.buffer
        snippet = snippets[trigger]
        cur_text = cur_text[: len(cur_text) - len(trigger)]
        next_text = self._vim.call('deoppet#util#_get_next_text')
        # debug(self._vim, cur_text)
        # debug(self._vim, snippet['trigger'])
        # debug(self._vim, next_text)

        texts = snippet['text'].split('\n')
        buf[linenr-1] = cur_text + texts[0] + next_text
        if len(texts) > 1:
            lastnr = linenr + len(texts) - 2
            buf[linenr:lastnr - 1] = texts[1:-1]
            buf[lastnr + 1:] = buf[lastnr:]
            buf[lastnr] = texts[-1]

        col = self._vim.call('len', cur_text + texts[0])

        ids = []
        self._ns = self._vim.call('nvim_create_namespace', 'deoppet')
        debug(self._vim, snippet['tabstops'])
        for tabstop in snippet['tabstops']:
            ids.append(self._vim.call('nvim_buf_set_extmark',
                                      buf.number, self._ns, 0,
                                      tabstop['row'] + linenr - 1,
                                      tabstop['col'], {}))
        bvars['deoppet_marks'] = ids + bvars['deoppet_marks']
        self.cursor(linenr, col, next_text)

    def jump(self, is_forward: bool) -> None:
        bvars = self._vim.current.buffer.vars
        if not bvars['deoppet_marks']:
            self.nop()
            return
        buf = self._vim.current.buffer
        marks = bvars['deoppet_marks']
        mark = self._vim.call('nvim_buf_get_extmark_by_id',
                              buf.number, self._ns, marks[0])
        next_text = buf[mark[0]][mark[1]:]
        self.cursor(mark[0] + 1, mark[1], next_text)
        bvars['deoppet_marks'] = marks[1:] + [marks[0]]

    def nop(self) -> None:
        return self.cursor(self._vim.current.window.cursor[0],
                           self._vim.current.window.cursor[1],
                           self._vim.call('deoppet#util#_get_next_text'))

    def cursor(self, linenr: int, col: int, next_text: str) -> None:
        # self.debug(next_text)
        if next_text:
            self._vim.call('cursor', [linenr, col + 1])
            self._vim.command('startinsert')
        else:
            self._vim.call('cursor', [linenr, col])
            self._vim.command('startinsert!')
