# ============================================================================
# FILE: __init__.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import typing

from importlib.util import find_spec

if find_spec('yarp'):
    import vim
elif find_spec('pynvim'):
    import pynvim as vim
    from pynvim import Nvim

if hasattr(vim, 'plugin'):
    # Neovim only

    from deoppet.deoppet import Deoppet

    @vim.plugin
    class DeoppetHandlers(object):

        def __init__(self, vim: Nvim) -> None:
            self._vim = vim

        @vim.function('_deoppet_init', sync=False)  # type: ignore
        def init_channel(self, args: typing.List[str]) -> None:
            self._vim.vars['deoppet#_channel_id'] = self._vim.channel_id
            self._deoppet = Deoppet(self._vim)

        @vim.function('_deoppet_expand', sync=True)  # type: ignore
        def expand(self, args: typing.List[str]) -> None:
            self._deoppet.expand(args[0])

        @vim.function('_deoppet_mapping', sync=True)  # type: ignore
        def mapping(self, args: typing.List[str]) -> None:
            self._deoppet.mapping(args[0], args[1])

        @vim.function('_deoppet_event', sync=True)  # type: ignore
        def event(self, args: typing.List[str]) -> None:
            self._deoppet.event(args[0])
