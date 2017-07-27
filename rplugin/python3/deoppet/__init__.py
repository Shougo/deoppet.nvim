# ============================================================================
# FILE: __init__.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import neovim
from deoppet.deoppet import Deoppet


@neovim.plugin
class DeoppetHandlers(object):

    def __init__(self, vim):
        self._vim = vim

    @neovim.function('_deoppet', sync=False)
    def init_channel(self, args):
        self._vim.vars['deoppet#_channel_id'] = self._vim.channel_id
        self._deoppet = Deoppet(self._vim)
