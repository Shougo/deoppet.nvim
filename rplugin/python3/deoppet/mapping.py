# ============================================================================
# FILE: mapping.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import copy
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
        self._ns = self._vim.api.create_namespace('deoppet')
        buf = self._vim.current.buffer
        bvars = buf.vars
        if 'deoppet_tabstops' not in bvars:
            return

        for tabstop in bvars['deoppet_tabstops']:
            buf.api.del_extmark(self._ns, tabstop['id_begin'])
            buf.api.del_extmark(self._ns, tabstop['id_end'])

        bvars['deoppet_tabstops'] = []
        bvars['deoppet_mark_pos'] = 0
        bvars['deoppet_snippet'] = {}

    def mapping(self, name: str) -> None:
        bvars = self._vim.current.buffer.vars
        if 'deoppet_tabstops' not in bvars:
            bvars['deoppet_tabstops'] = []
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
        self.clear()

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
        buf[linenr - 1] = cur_text + texts[0] + next_text
        if len(texts) > 1:
            lastnr = linenr + len(texts) - 2
            buf[linenr:lastnr - 1] = texts[1:-1]
            buf[lastnr + 1:] = buf[lastnr:]
            if len(buf) > lastnr:
                buf[lastnr] = texts[-1]
            else:
                buf.append(texts[-1])

        col = self._vim.call('len', cur_text + texts[0])

        tabstops = []
        self._ns = self._vim.api.create_namespace('deoppet')
        for tabstop in copy.deepcopy(snippet['tabstops']):
            mark_id = buf.api.set_extmark(
                self._ns, 0,
                tabstop['row'] + linenr - 1, tabstop['col'], {})
            tabstop['id_begin'] = mark_id
            tabstop['id_end'] = mark_id
            tabstops.append(tabstop)

        bvars['deoppet_tabstops'] = tabstops
        bvars['deoppet_mark_pos'] = 0
        bvars['deoppet_snippet'] = snippet

        self.cursor(linenr, col, next_text)

        # Jump forward
        return self.jump(True)

    def jump(self, is_forward: bool) -> None:
        bvars = self._vim.current.buffer.vars
        if not bvars['deoppet_tabstops']:
            self.nop()
            return

        buf = self._vim.current.buffer
        tabstops = bvars['deoppet_tabstops']
        tabstop = tabstops[bvars['deoppet_mark_pos']]
        mark_begin = buf.api.get_extmark_by_id(self._ns, tabstop['id_begin'])
        if not mark_begin or mark_begin[0] >= len(buf):
            # Overflow
            return
        next_text = buf[mark_begin[0]][mark_begin[1]:]
        self.cursor(mark_begin[0] + 1, mark_begin[1], next_text)

        # Default
        pos = bvars['deoppet_mark_pos']
        if tabstop['default']:
            mark_end = buf.api.get_extmark_by_id(
                self._ns, tabstop['id_end'])
            debug(self._vim, mark_begin)
            debug(self._vim, mark_end)
            if mark_begin == mark_end:
                self._vim.call('deoppet#util#_select_text',
                               tabstop['default'])

                # Update marks
                buf.api.del_extmark(self._ns, tabstop['id_begin'])
                buf.api.del_extmark(self._ns, tabstop['id_end'])
                tabstop['id_begin'] = buf.api.set_extmark(
                    self._ns, 0, mark_begin[0], mark_begin[1], {})
                tabstop['id_end'] = buf.api.set_extmark(
                    self._ns, 0, mark_begin[0],
                    self._vim.call('col', '.') - 1, {})
                bvars['deoppet_tabstops'] = tabstops
            else:
                # Select begin to end.
                self._vim.call('deoppet#util#_select_pos', mark_end)

        # Update position
        next_pos = pos
        if is_forward:
            next_pos += 1
        else:
            next_pos -= 1
        if next_pos < 0:
            next_pos = len(tabstops) - 1
        elif next_pos >= len(tabstops):
            next_pos = 0
        bvars['deoppet_mark_pos'] = next_pos

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
