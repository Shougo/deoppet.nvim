# ============================================================================
# FILE: parser.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import re
import typing

Snippet = typing.Dict[str, typing.Any]


class Parser():

    def __init__(self) -> None:
        self.lines: typing.List[str] = []
        self.linenr = 0
        self.line_max = 0
        pass

    def parse(self, text: str) -> Snippet:
        self.lines = text.splitlines()
        self.linenr = 0
        self.line_max = len(self.lines)

        snippets: typing.Dict[str, Snippet] = {}
        while self.linenr < self.line_max:
            line = self.lines[self.linenr]
            if re.search(r'^\s*#|^\s*$', line):
                # Skip
                self.linenr += 1
                continue
            if not re.search(r'^\s*snippet\s+', line):
                # Error
                return {}

            snippet = self.parse_one_snippet()
            if not snippet:
                # Error
                return {}
            snippets[snippet['trigger']] = snippet
        return snippets

    def parse_one_snippet(self) -> Snippet:
        line = self.lines[self.linenr]
        m = re.search(r'^\s*snippet\s+(.*)$', line)
        if not m:
            return {}

        snippet: Snippet = {}
        snippet['trigger'] = m.group(1)
        snippet['text'] = ''
        snippet['options'] = {}
        snippet['tabstops'] = []

        # Parse the next line
        while (self.linenr + 1) < self.line_max:
            self.linenr += 1

            line = self.lines[self.linenr]
            m = re.search(r'^abbr\s+(\S+)', line)
            if m:
                snippet['abbr'] = m.group(1)
                continue

            m = re.search(r'^alias\s+(\S+)', line)
            if m:
                snippet['alias'] = m.group(1)
                continue

            m = re.search(r"^regexp\s+'([^']+)'", line)
            if m:
                snippet['regexp'] = m.group(1)
                continue

            m = re.search(r'^options\s+(\S+)', line)
            if m:
                for option in m.group(1).split(' '):
                    snippet['options'][option] = True
                continue

            m = re.search(r'^\s+(.*)$', line)
            if m:
                return self.parse_text(snippet)

            # Error
            break

        # Error
        return {}

    def parse_text(self, snippet: Snippet) -> Snippet:
        text_linenr = 0
        while self.linenr < self.line_max:
            line = self.lines[self.linenr]
            m = re.search(r'^\s+(.*)$', line)
            if not m:
                return snippet

            # Substitute tabstops
            line = m.group(1)
            while 1:
                [tabstop, line] = self.parse_tabstop(line, text_linenr)
                if not tabstop:
                    break

                snippet['tabstops'].append(tabstop)

            snippet['text'] += line
            self.linenr += 1
            text_linenr += 1
        return snippet

    def parse_tabstop(self, line: str, text_linenr: int
                      ) -> typing.List[typing.Any]:
        m = re.search(r'\${(\d+)}', line)
        if not m:
            return [{}, line]

        return [
            {
                'number': int(m.group(1)),
                'row': text_linenr,
                'col': m.start(),
                'default': '',
            },
            re.sub(r'\${(\d+)}', '', line, count=1)
        ]
