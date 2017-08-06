import sys
print(sys.path)
from deoppet.parser import Parser

def test_parse():
    parser = Parser()

    test_snippet = """
snippet    foo
abbr       bar
alias      baz
regexp     '^% '
options    word
   foobar
"""
    assert parser.parse(test_snippet) == [{
        'name': 'foo',
        'abbr': 'bar',
        'alias': ['baz'],
        'regexp': '^% ',
        'options': ['word'],
        'text': 'foobar',
    }]
