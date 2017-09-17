#=============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
#=============================================================================

from .base import Base
from deoppet.parser import Parser
from deoppet.util import globruntime, debug


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'deoppet'
        self.mark = '[dp]'
        self.rank = 200

    def gather_candidates(self, context):
        return []

        parser = Parser()
        snippets = []

        for filename in globruntime(self.vim.options['runtimepath'],
                                    'neosnippets/*.snip'):
            # debug(self._vim, filename)
            with open(filename) as f:
                snippets += parser.parse(f.read())
        return [{'word': x['trigger']} for x in snippets]
