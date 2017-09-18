# ============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from deoppet.parser import Parser
from deoppet.util import globruntime
# from deoppet.util import debug


class Deoppet():

    def __init__(self, vim):
        self._vim = vim
        self._parser = Parser()
        self._snippets = {}

        for filename in globruntime(self._vim.options['runtimepath'],
                                    'neosnippets/*.snip'):
            # debug(self._vim, filename)
            with open(filename) as f:
                self._snippets.update(self._parser.parse(f.read()))
        self._vim.current.buffer.vars['deoppet_snippets'] = self._snippets
