import collections
import re

def lex_id(input):
    m = re.match(r':?[a-zA-Z_]+[\w-]*[!?_]?:?', input)
    if not m:
        return

    type_ = 'ID'
    end = input[m.end() - 1]
    if input.startswith(':'):
        if end == ':':
            return
        type_ = 'ARGUMENT'
    elif end == ':':
        type_ = 'KEYWORD'
    return type_, m.end()

def lex_number(input):
    m = re.match(r'-?\d+(\.\d)?', input)
    if m:
        return 'NUMBER', m.end()

def lex_operator(input):
    m = re.match(r'[!@#$%^&*\-+=~/?<>|:]+', input)
    if m:
        return 'OPERATOR', m.end()

def lex_string(input):
    m = input.startswith("'") and re.search(r"[^\\]'", input, 1)
    if m:
        return 'STRING', m.end() 

def lex_whitespace(input):
    m = re.match(r'\s+', input)
    if m:
        return None, m.end()

Token = collections.namedtuple('Token', 'type value position')

def lex(input):
    pos = 0
    while input: 
        tok = None
        for lex_ in [lex_id, lex_number, lex_operator, lex_string, lex_whitespace]:
            tok = lex_(input)
            if tok:
                type_, len_ = tok
                if type_:
                    yield Token(type_, input[:len_], pos)

                pos += len_ 
                input = input[len_:]
                break
            
        if input and not tok:
            raise NameError(input)
