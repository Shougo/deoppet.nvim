# ============================================================================
# FILE: mapping.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import copy
import re
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
        self._vim.vars['deoppet#captures'] = []

    def mapping(self, name: str) -> None:
        bvars = self._vim.current.buffer.vars
        if 'deoppet_tabstops' not in bvars:
            bvars['deoppet_tabstops'] = []
        if 'deoppet_snippets' not in bvars:
            return

        if name == 'clear':
            return self.clear()
        if name == 'expand':
            return self.expand_current_trigger()
        if name == 'jump_forward':
            return self.jump(True)
        if name == 'jump_backward':
            return self.jump(False)
        return

    def expand_current_trigger(self) -> None:
        self.clear()

        bvars = self._vim.current.buffer.vars
        snippets = bvars['deoppet_snippets']
        cur_text = self._vim.call('deoppet#util#_get_cur_text')
        trigger = self._vim.call('deoppet#util#_get_cursor_snippet',
                                 snippets, cur_text)
        if not trigger:
            return

        snippet = snippets[trigger]
        if snippet['regexp']:
            if not self._vim.call(
                    'matchstr', cur_text, snippet['regexp']):
                # Not matched regexp
                return

            # Capture
            self._vim.vars['deoppet#captures'] = self._vim.call(
                'matchlist', cur_text, snippet['regexp'])

        prev_text = cur_text[: len(cur_text) - len(trigger)]
        return self.expand(trigger, prev_text)

    def expand(self, trigger: str, prev_text: str) -> None:
        bvars = self._vim.current.buffer.vars
        if 'deoppet_snippets' not in bvars:
            return

        snippets = bvars['deoppet_snippets']

        if not trigger or trigger not in snippets:
            return

        snippet = snippets[trigger]

        # Expand trigger
        cursor = self._vim.current.window.cursor
        linenr = cursor[0]
        col = cursor[1]
        buf = self._vim.current.buffer
        next_text = self._vim.call('deoppet#util#_get_next_text')

        base_indent = ''
        m = re.match(r'\s+', prev_text)
        if m:
            base_indent = m.group(0)

        texts = [(base_indent if num != 0 else '') + x for num, x
                 in enumerate(snippet['text'].split('\n'))]
        buf[linenr - 1] = prev_text + texts[0] + next_text
        if len(texts) > 1:
            lastnr = linenr + len(texts) - 2
            if len(buf) > lastnr:
                buf[lastnr:] = texts[1:] + buf[lastnr:]
            else:
                buf.append(texts[1:])

        col = self._vim.call('len', prev_text + texts[0])

        tabstops = []
        evals = []
        self._ns = self._vim.api.create_namespace('deoppet')
        for tabstop in copy.deepcopy(snippet['tabstops']):
            tabstop_col = tabstop['col']
            if tabstop['row'] == 0:
                tabstop_col += self._vim.call('len', prev_text)
            else:
                tabstop_col += len(base_indent)
            mark_id = buf.api.set_extmark(
                self._ns, 0,
                tabstop['row'] + linenr - 1, tabstop_col, {})
            tabstop['id_begin'] = mark_id
            tabstop['id_end'] = mark_id
            tabstops.append(tabstop)
        for ev in copy.deepcopy(snippet['evals']):
            ev_col = ev['col']
            if ev['row'] == 0:
                ev_col += self._vim.call('len', prev_text)
            mark_id = buf.api.set_extmark(
                self._ns, 0,
                ev['row'] + linenr - 1, ev_col, {})
            ev['id_begin'] = mark_id
            ev['id_end'] = mark_id
            evals.append(ev)

        bvars['deoppet_tabstops'] = tabstops
        bvars['deoppet_mark_pos'] = 0
        bvars['deoppet_snippet'] = snippet

        self.cursor(linenr, col, next_text)

        # Expand evals
        for ev in evals:
            self.expand_eval(ev)

        # Indentation
        self._vim.call('deoppet#util#_indent_snippet',
                       linenr + 1, linenr + len(texts) - 1)

        # Jump forward
        return self.jump(True)

    def expand_eval(self, ev: typing.Dict[str, typing.Any]) -> None:
        buf = self._vim.current.buffer
        mark_begin = buf.api.get_extmark_by_id(self._ns, ev['id_begin'])
        if not mark_begin or mark_begin[0] >= len(buf):
            # Overflow
            return
        next_text = buf[mark_begin[0]][mark_begin[1]:]
        self.cursor(mark_begin[0] + 1, mark_begin[1], next_text)

        self._vim.call('deoppet#util#_insert_text',
                       self._vim.call('eval', ev['expr']))

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
        if next_text:
            self._vim.call('cursor', [linenr, col + 1])
            self._vim.command('startinsert')
        else:
            self._vim.call('cursor', [linenr, col])
            self._vim.command('startinsert!')
