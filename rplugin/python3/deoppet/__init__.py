# ============================================================================
# FILE: __init__.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import neovim
from deoppet.deoppet import Deoppet
from deoppet.mapping import Mapping
# from deoppet.util import debug


@neovim.plugin
class DeoppetHandlers(object):

    def __init__(self, vim):
        self._vim = vim

    @neovim.function('_deoppet_initialize', sync=False)
    def init_channel(self, args):
        self._vim.vars['deoppet#_channel_id'] = self._vim.channel_id
        self._deoppet = Deoppet(self._vim)
        self._mapping = Mapping(self._vim)

        # Initialize mappings
        self._vim.call('deoppet#mappings#_init')

    @neovim.function('_deoppet_mapping', sync=True)
    def mapping(self, args):
        self._mapping.mapping(args[0])
