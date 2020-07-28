import sys
print(sys.path)
from deoppet.parser import Parser
from unittest.mock import Mock

def test_parse_success():
    vim = Mock()
    parser = Parser(vim)

    test_snippet0 = """
"""

    assert parser.parse(test_snippet0) == {}

    test_snippet1 = """
snippet    foo
   foobar
"""

    assert parser.parse(test_snippet1) == {
        'foo': {
            'trigger': 'foo',
            'text': 'foobar',
            'regexp': '',
            'options': {},
            'tabstops': [],
            'evals': [],
        }
    }

    test_snippet2 = """
snippet    foo
   foobar

snippet    bar
   baz
"""

    assert parser.parse(test_snippet2) == {
        'foo': {
            'trigger': 'foo',
            'text': 'foobar',
            'regexp': '',
            'options': {},
            'tabstops': [],
            'evals': [],
        },
        'bar': {
            'trigger': 'bar',
            'text': 'baz',
            'regexp': '',
            'options': {},
            'tabstops': [],
            'evals': [],
        }
    }

    test_snippet3 = """
snippet    foo
abbr       bar
alias      baz
regexp     '^% '
options    word
   foobar
"""

    assert parser.parse(test_snippet3) == {
        'foo': {
            'trigger': 'foo',
            'abbr': 'bar',
            'alias': 'baz',
            'regexp': '^% ',
            'options': {'word': True},
            'text': 'foobar',
            'tabstops': [],
            'evals': [],
        }
    }

    test_snippet4 = """
snippet    foo
   foobar ${1} ${2}
"""

    assert parser.parse(test_snippet4) == {
        'foo': {
            'trigger': 'foo',
            'text': 'foobar  ',
            'regexp': '',
            'options': {},
            'tabstops': [
                {'number': 1, 'row': 0, 'col': 7, 'default': '', 'comment': ''},
                {'number': 2, 'row': 0, 'col': 8, 'default': '', 'comment': ''},
            ],
            'evals': [],
        }
    }

    test_snippet5 = """
snippet     if
abbr        if endif
options     head
    if ${1:#:condition}
      ${0:TARGET}
    endif

snippet     elseif
options     head
    elseif condition
        TARGET
"""

    assert parser.parse(test_snippet5) == {
        'if': {
            'abbr': 'if endif',
            'trigger': 'if',
            'text': 'if \n\nendif',
            'regexp': '',
            'options': {'head': True},
            'tabstops': [
                {
                    'number': 1, 'row': 0, 'col': 3,
                    'default': '#:condition', 'comment': ''
                 },
                {
                    'number': 0, 'row': 1, 'col': 0,
                    'default': 'TARGET', 'comment': ''
                },
            ],
            'evals': [],
        },
        'elseif': {
            'trigger': 'elseif',
            'text': 'elseif condition\nTARGET',
            'regexp': '',
            'options': {'head': True},
            'tabstops': [
            ],
            'evals': [],
        }
    }

def test_parse_error():
    vim = Mock()
    parser = Parser(vim)

    test_snippet0 = """
snippet bar
"""

    assert parser.parse(test_snippet0) == {}
