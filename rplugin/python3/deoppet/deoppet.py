# ============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from deoppet.parser import Parser


class Deoppet():

    def __init__(self, vim):
        self._vim = vim
        self._parser = Parser()
