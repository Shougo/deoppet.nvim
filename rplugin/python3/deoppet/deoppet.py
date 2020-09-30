# ============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import copy
import glob
import typing

from deoppet.parser import Parser, Snippet
from deoppet.mapping import Mapping
from deoppet.util import debug

from pynvim import Nvim


class Deoppet():

    def __init__(self, vim: Nvim) -> None:
        self._vim = vim
        if not self._vim.call('has', 'nvim-0.5.0'):
            return

        self._mapping = Mapping(self._vim)

        self._vim.call('deoppet#custom#_update_cache')

        self._load_snippets()

        self._vim.call('deoppet#mapping#_init')
        self._vim.call('deoppet#handler#_init')

    def debug(self, expr: typing.Any) -> None:
        debug(self._vim, expr)

    def mapping(self, name: str, cur_text: str) -> None:
        return self._mapping.mapping(name, cur_text)

    def expand(self, trigger: str) -> None:
        return self._mapping.expand(
            trigger, self._vim.call('deoppet#util#_get_cur_text'))

    def event(self, name: str) -> None:
        self._vim.call('deoppet#custom#_update_cache')

        if name == 'FileType':
            return self._load_snippets()
        else:
            return self._mapping.clear()

    def _load_snippets(self) -> None:
        buf = self._vim.current.buffer
        filetype: str = self._vim.call(
            'deoppet#util#_get_context_filetype')
        if not filetype:
            filetype = 'nothing'
        snippets_dirs = self._vim.call(
            'deoppet#custom#_get_option', 'snippets_dirs')
        ft_snippets_map = self._vim.call(
            'deoppet#custom#_get_option', 'ft_snippets_map')
        if filetype in ft_snippets_map:
            fts = ft_snippets_map[filetype]
        else:
            fts = filetype.split(',')

        snippets: typing.Dict[str, Snippet] = {}
        for dir in snippets_dirs:
            for ft in fts:
                for filename in glob.glob(
                        f'{dir}/{ft}.snip') + glob.glob(f'{dir}/_.snip'):
                    # debug(self._vim, filename)
                    with open(filename) as f:
                        parser = Parser(self._vim, filename)
                        snippets.update(parser.parse(f.read()))

        for s in copy.deepcopy(snippets).values():
            for a in s.get('alias', []):
                snippets[a] = s
        # debug(self._vim, snippets)
        buf.vars['deoppet_snippets'] = snippets
