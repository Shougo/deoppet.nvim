from deoplete.parser import Parser

def test_parse():
    parser = Parser()
    assert util.bytepos2charpos('utf-8', 'foo bar', 3) == 3
