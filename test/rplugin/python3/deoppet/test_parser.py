import sys
print(sys.path)
from deoppet.parser import Parser

def test_parse():
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

    assert parser.parse(test_snippet0) == []

    assert parser.parse(test_snippet1) == [{
        'trigger': 'foo',
        'text': 'foobar',
    }]

    assert parser.parse(test_snippet2) == [
        {
            'trigger': 'foo',
            'text': 'foobar',
        },
        {
            'trigger': 'bar',
            'text': 'baz',
        }
    ]

    assert parser.parse(test_snippet3) == [{
        'trigger': 'foo',
        'abbr': 'bar',
        'alias': 'baz',
        'regexp': '^% ',
        'options': ['word'],
        'text': 'foobar',
    }]
