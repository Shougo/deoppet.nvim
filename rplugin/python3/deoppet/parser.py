# ============================================================================
# FILE: parser.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import re


class Parser():

    def __init__(self):
        self.lines = []
        self.linenr = 0
        self.line_max = 0
        pass

    def parse(self, text):
        self.lines = text.splitlines()
        self.linenr = 0
        self.line_max = len(self.lines)

        snippets = []
        while self.linenr < self.line_max:
            line = self.lines[self.linenr]
            if re.search('^\s*#|^\s*$', line):
                # Skip
                self.linenr += 1
                continue
            if not re.search('^\s*snippet\s+', line):
                # Error
                return []

            snippet = self.parse_one_snippet()
            return [snippet]
            if not snippet:
                # Error
                return []
            snippets.append(snippet)
        return snippets

    def parse_one_snippet(self):
        line = self.lines[self.linenr]
        snippet = {}
        m = re.search('^\s*snippet\s+(.*)$', line)
        if not m:
            return {}
        snippet['trigger'] = m.group(1)
        snippet['text'] = ''

        self.linenr += 1
        while self.linenr < self.line_max:
            line = self.lines[self.linenr]
            if re.search('^\s*(\S+)', line):
                return self.parse_text(snippet)

            line += 1

        # Error
        return {}

    def parse_text(self, snippet):
        while self.linenr < self.line_max:
            line = self.lines[self.linenr]
            m = re.search('^\s*(\S+)', line)
            if not m:
                return snippet

            snippet['text'] += m.group(1)
            self.linenr += 1
        return snippet
