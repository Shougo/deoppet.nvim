# ============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from deoppet.parser import Parser
from deoppet.util import globruntime, debug


class Deoppet():

    def __init__(self, vim):
        self._vim = vim
        self._parser = Parser()
        self._snippets = []

        for filename in globruntime(self._vim.options['runtimepath'],
                                    'neosnippets/*.snip'):
            # debug(self._vim, filename)
            with open(filename) as f:
                self._snippets += self._parser.parse(f.read())
        debug(self._vim, self._snippets)
