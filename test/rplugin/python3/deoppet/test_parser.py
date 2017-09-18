import sys
print(sys.path)
from deoppet.parser import Parser

def test_parse_success():
    parser = Parser()

    test_snippet0 = """
"""

    test_snippet1 = """
snippet    foo
   foobar
"""

    test_snippet2 = """
snippet    foo
   foobar

snippet    bar
   baz
"""

    test_snippet3 = """
snippet    foo
abbr       bar
alias      baz
regexp     '^% '
options    word
   foobar
"""

    assert parser.parse(test_snippet0) == {}

    assert parser.parse(test_snippet1) == {
        'foo': {
            'trigger': 'foo',
            'text': 'foobar',
            'options': {},
        }
    }

    assert parser.parse(test_snippet2) == {
        'foo': {
            'trigger': 'foo',
            'text': 'foobar',
            'options': {},
        },
        'bar': {
            'trigger': 'bar',
            'text': 'baz',
            'options': {},
        }
    }

    assert parser.parse(test_snippet3) == {
        'foo': {
            'trigger': 'foo',
            'abbr': 'bar',
            'alias': 'baz',
            'regexp': '^% ',
            'options': {'word': True},
            'text': 'foobar',
        }
    }

def test_parse_error():
    parser = Parser()

    test_snippet0 = """
snippet bar
"""

    assert parser.parse(test_snippet0) == {}
