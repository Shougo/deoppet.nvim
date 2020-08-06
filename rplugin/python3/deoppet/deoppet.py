# ============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import glob
import typing

from deoppet.parser import Parser, Snippet
from deoppet.mapping import Mapping
# from deoppet.util import debug

from pynvim import Nvim


class Deoppet():

    def __init__(self, vim: Nvim) -> None:
        self._vim = vim
        if not self._vim.call('has', 'nvim-0.5.0'):
            return

        self._mapping = Mapping(self._vim)
        self._options = self._vim.call('deoppet#custom#_get')['option']

        self._load_snippets()

        self._vim.call('deoppet#mapping#_init')
        self._vim.call('deoppet#handler#_init')

    def mapping(self, name: str) -> None:
        return self._mapping.mapping(name)

    def expand(self, trigger: str) -> None:
        return self._mapping.expand(
            trigger, self._vim.call('deoppet#util#_get_cur_text'))

    def event(self, name: str) -> None:
        if name == 'FileType':
            return self._load_snippets()
        else:
            return self._mapping.clear()

    def _load_snippets(self) -> None:
        snippets: typing.Dict[str, Snippet] = {}
        buf = self._vim.current.buffer
        filetype: str = self._vim.call(
            'getbufvar', buf.number, '&filetype')
        if not filetype:
            filetype = 'nothing'
        # debug(self._vim, filetype)
        # debug(self._vim, self._vim.current.buffer.number)
        for dir in self._options['snippets_dirs']:
            for filename in glob.glob(
                    f'{dir}/{filetype}.snip') + glob.glob(f'{dir}/_.snip'):
                # debug(self._vim, filename)
                with open(filename) as f:
                    parser = Parser(self._vim, filename)
                    snippets.update(parser.parse(f.read()))
        # debug(self._vim, snippets)
        buf.vars['deoppet_snippets'] = snippets
