# ============================================================================
# FILE: mapping.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

# from deoppet.util import debug


class Mapping():

    def __init__(self, vim):
        self._vim = vim

    def mapping(self, name):
        if name == 'expand':
            return self.expand()
        if name == 'jump_forward':
            return self.jump(True)
        if name == 'jump_backward':
            return self.jump(False)
        return

    def expand(self):
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

    def jump(self, is_forward):
        bvars = self._vim.current.buffer.vars
        if 'deoppet_marks' not in bvars:
            return
