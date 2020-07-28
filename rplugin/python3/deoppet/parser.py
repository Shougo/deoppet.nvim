# ============================================================================
# FILE: parser.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import re
import typing

# from deoppet.util import debug
from pynvim import Nvim

Snippet = typing.Dict[str, typing.Any]


class Parser():

    def __init__(self, vim: Nvim) -> None:
        self._vim = vim

        self._lines: typing.List[str] = []
        self._linenr = 0
        self._line_max = 0

    def parse(self, text: str) -> Snippet:
        self._lines = text.splitlines()
        self._linenr = 0
        self._line_max = len(self._lines)

        snippets: typing.Dict[str, Snippet] = {}
        while self._linenr < self._line_max:
            line = self._lines[self._linenr]
            if re.search(r'^\s*#|^\s*$', line):
                # Skip
                self._linenr += 1
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
        line = self._lines[self._linenr]
        m = re.search(r'^\s*snippet\s+(.*)$', line)
        if not m:
            return {}

        snippet: Snippet = {}
        snippet['trigger'] = m.group(1)
        snippet['text'] = ''
        snippet['regexp'] = ''
        snippet['options'] = {}
        snippet['tabstops'] = []
        snippet['evals'] = []

        # Parse the next line
        while (self._linenr + 1) < self._line_max:
            self._linenr += 1

            line = self._lines[self._linenr]
            m = re.search(r'^abbr\s+(.*)', line)
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
        while self._linenr < self._line_max:
            line = self._lines[self._linenr]
            if not line:
                # Skip
                if snippet['text']:
                    snippet['text'] += '\n'
                self._linenr += 1
                text_linenr += 1
                continue

            m = re.search(r'^\s+(.*)$', line)
            if not m:
                break

            # Substitute tabstops
            line = m.group(1)
            while 1:
                prev_line = line

                [ev, line] = self.parse_eval(line, text_linenr)
                if ev:
                    snippet['evals'].append(ev)

                [tabstop, line] = self.parse_tabstop(line, text_linenr)
                if tabstop:
                    snippet['tabstops'].append(tabstop)

                if prev_line == line:
                    break

            if snippet['text']:
                snippet['text'] += '\n'
            snippet['text'] += line
            self._linenr += 1
            text_linenr += 1

        # Chomp the last "\n"
        if snippet['text'] and snippet['text'][-1] == '\n':
            snippet['text'] = snippet['text'][:-1]
        return snippet

    def parse_tabstop(self, line: str, text_linenr: int
                      ) -> typing.List[typing.Any]:
        pattern = r'\${((\d+)(:([^}]*|:#:[^}]*|TARGET))?)}'
        m = re.search(pattern, line)
        if not m:
            return [{}, line]

        default = m.group(4)
        if not default:
            default = ''
        return [
            {
                'number': int(m.group(2)),
                'row': text_linenr,
                'col': m.start(),
                'default': default,
                'comment': '',
            },
            re.sub(pattern, '', line, count=1)
        ]

    def parse_eval(self, line: str, text_linenr: int
                   ) -> typing.List[typing.Any]:
        pattern = r'`([^`]+)`'
        m = re.search(pattern, line)
        if not m:
            return [{}, line]

        eval_expr = m.group(1)
        if not eval_expr:
            eval_expr = ''
        return [
            {
                'row': text_linenr,
                'col': m.start(),
                'expr': eval_expr,
            },
            re.sub(pattern, '', line, count=1)
        ]
