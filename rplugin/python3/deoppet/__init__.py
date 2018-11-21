# ============================================================================
# FILE: __init__.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from importlib.util import find_spec

if find_spec('yarp'):
    import vim
elif find_spec('pynvim'):
    import pynvim
    vim = pynvim
else:
    import neovim
    vim = neovim

if hasattr(vim, 'plugin'):
    # Neovim only

    from deoppet.deoppet import Deoppet

    @vim.plugin
    class DeoppetHandlers(object):

        def __init__(self, vim):
            self._vim = vim

        @vim.function('_deoppet_initialize', sync=False)
        def init_channel(self, args):
            self._vim.vars['deoppet#_channel_id'] = self._vim.channel_id
            self._deoppet = Deoppet(self._vim)

        @vim.function('_deoppet_mapping', sync=True)
        def mapping(self, args):
            self._deoppet.mapping(args[0])

        @vim.function('_deoppet_event', sync=True)
        def event(self, args):
            self._deoppet.event(args[0])
