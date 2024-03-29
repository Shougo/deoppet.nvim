# ============================================================================
# FILE: parser.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import glob
import re
import typing

from deoppet.util import debug
from pynvim import Nvim

Snippet = typing.Dict[str, typing.Any]


class Parser():

    def __init__(self, vim: Nvim, filename: str,
                 snippets_dirs: typing.List[str]) -> None:
        self._vim = vim

        self._lines: typing.List[str] = []
        self._linenr = 0
        self._line_max = 0
        self._filename = filename
        self._snippets_dirs = snippets_dirs

    def debug(self, expr: typing.Any) -> None:
        debug(self._vim, expr)

    def error(self, expr: typing.Any) -> None:
        self._vim.call('deoppet#util#print_error',
                       f'{self._filename}:{self._linenr} ' + str(expr))

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

            m = re.search(r'^\s*delete\s+(\S+)$', line)
            if m:
                # Delete snippet trigger
                s = m.group(1)
                if s in snippets:
                    del snippets[s]
                else:
                    self.error(f'try to delete a non-existing snippet {s}')
                self._linenr += 1
                continue
            m = re.search(r'^\s*extends\s+(\S+)$', line)
            if m:
                # Extend snippets files.
                for ft in m.group(1).split(r'\s*,\s*'):
                    for snip in [ft + '.snip', ft + '.snippets', ft + '/*']:
                        snippets.update(self.include_snippets(snip))
                self._linenr += 1
                continue
            m = re.search(r'^\s*include\s+(\S+)$', line)
            if m:
                # Include snippets file.
                snippets.update(self.include_snippets(m.group(1)))
                self._linenr += 1
                continue
            m = re.search(r'^\s*source\s+(\S+)$', line)
            if m:
                # Source Vim script file.
                base = m.group(1)
                for dir in self._snippets_dirs:
                    for filename in glob.glob(f'{dir}/{base}'):
                        self._vim.command(f'source {filename}')
                self._linenr += 1
                continue

            if re.search(r'^\s*snippet\s+', line):
                snippet = self.parse_one_snippet()
                if not snippet:
                    # Error
                    self.error(f'parse error in: {line}')
                    return {}

                snippets[snippet['trigger']] = snippet
                continue

            # Error
            self.error(f'parse error in: {line}')
            return {}
        return snippets

    def include_snippets(self, base: str) -> typing.Dict[str, Snippet]:
        snippets: typing.Dict[str, Snippet] = {}

        for dir in self._snippets_dirs:
            for filename in glob.glob(f'{dir}/{base}'):
                # debug(self._vim, filename)
                with open(filename) as f:
                    parser = Parser(self._vim,
                                    filename, self._snippets_dirs)
                    snippets.update(parser.parse(f.read()))
        return snippets

    def parse_one_snippet(self) -> Snippet:
        line = self._lines[self._linenr]
        m = re.search(r'^\s*snippet\s+(\S+)$', line)
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
            m = re.search(r'^abbr\s+(\S.*)', line)
            if m:
                snippet['abbr'] = m.group(1)
                continue

            m = re.search(r'^alias\s+(\S.*)', line)
            if m:
                snippet['alias'] = [a for a in re.split(r',|\s+', m.group(1))
                                    if a]
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

            m = re.search(r'^(\s+).*$', line)
            if m:
                return self.parse_text(snippet, m.group(1))

            # Error
            break

        # Error
        return {}

    def parse_text(self, snippet: Snippet, base_indent: str) -> Snippet:
        text_linenr = 0
        while self._linenr < self._line_max:
            line = self._lines[self._linenr]
            if not line:
                # Skip
                snippet['text'] += '\n'
                self._linenr += 1
                text_linenr += 1
                continue

            if not line.startswith(base_indent):
                break

            # Add new line
            if snippet['text']:
                snippet['text'] += '\n'

            # Substitute tabstops
            line = line[len(base_indent):]
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

            snippet['text'] += line
            self._linenr += 1
            text_linenr += 1

        if snippet['text'].endswith('\n'):
            snippet['text'] = snippet['text'][:-1]
        return snippet

    def parse_tabstop(self, line: str, text_linenr: int
                      ) -> typing.List[typing.Any]:
        pattern = r'\$\{(\d+)(?::(?:TARGET|#:.*?|(.*?)))?(?<!\\)\}'
        m = re.search(pattern, line)
        if not m:
            return [{}, line]

        default = m.group(2) or ''
        return [
            {
                'number': int(m.group(1)),
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
