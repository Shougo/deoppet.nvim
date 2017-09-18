# ============================================================================
# FILE: __init__.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import neovim
from deoppet.deoppet import Deoppet
# from deoppet.util import debug


@neovim.plugin
class DeoppetHandlers(object):

    def __init__(self, vim):
        self._vim = vim

    @neovim.function('_deoppet_initialize', sync=False)
    def init_channel(self, args):
        self._vim.vars['deoppet#_channel_id'] = self._vim.channel_id
        self._deoppet = Deoppet(self._vim)

        # Initialize mappings
        self._vim.call('deoppet#mappings#_init')

    @neovim.function('_deoppet_mapping', sync=True)
    def mapping(self, args):
        bvars = self._vim.current.buffer.vars
        if 'deoppet_snippets' not in bvars:
            return

        snippets = bvars['deoppet_snippets']
        cur_text = self._vim.call('deoppet#util#_get_cur_text')
        trigger = self._vim.call('deoppet#util#_get_cursor_snippet',
                                 snippets, cur_text)
        if not trigger:
            return

        # Expand trigger
        cursor = self._vim.current.window.cursor
        linenr = cursor[0]
        buf = self._vim.current.buffer
        snippet = snippets[trigger]
        next_text = self._vim.call('deoppet#util#_get_next_text')
        cur_text = cur_text[: len(cur_text) - len(trigger)]
        # debug(self._vim, cur_text)
        # debug(self._vim, snippet['trigger'])
        # debug(self._vim, next_text)
        buf[linenr-1] = cur_text + snippet['text'] + next_text
        col = self._vim.call('len', cur_text + snippet['text'])
        ns = self._vim.call('nvim_init_mark_ns', 'deoppet')
        ids = []
        for tabstop in snippet['tabstops']:
            ids.append(self._vim.call('nvim_buf_set_mark',
                                      buf.number, ns, 0,
                                      tabstop['row'] + linenr,
                                      tabstop['col'] + 1))
        bvars['deoppet_marks'] = ids
        if next_text:
            self._vim.call('cursor', [linenr, col + 1])
            self._vim.command('startinsert')
        else:
            self._vim.call('cursor', [linenr, col])
            self._vim.command('startinsert!')
