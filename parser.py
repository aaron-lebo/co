import ast

class Token(object):
    lbp = 0 

    def __init__(self, token=None):
        if token:
            self.value = token.value
            self.position = token.position
            self.args = [] 
   
    def __repr__(self):
        return '(%s)' % ', '.join(repr(x) for x in [self.value] + self.args)

class End(Token):
    pass 

class Literal(Token):
    def __init__(self, token):
        self.value = ast.literal_eval(token.value)

    def __repr__(self):
        return repr(self.value)

    def null(self, parser):
        return self

class Keyword(Token):
    lbp = 10 

    def null(self, parser):
        self.args = ['self', parser.expression(self.lbp - 1)]
        return self

    def left(self, left, parser):
        self.args = [left, parser.expression(self.lbp - 1)]
        return self

class Operator(Token):
    lbp = 20

    def __init__(self, token):
        super().__init__(token)
        if self.value in '*/%':
            self.lbp = 21
        elif self.value == '&&':
            self.lbp = 22
        elif self.value == '||':
            self.lbp = 23

    def null(self, parser):
        return parser.expression()

    def left(self, left, parser):
        self.args = [left, parser.expression(self.lbp)]
        return self

class Id(Token):
    lbp = 30 

    def null(self, parser):
        self.args = ['self']
        return self

    def left(self, left, parser):
        self.args = [left]
        return self

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.step()

    def step(self):
        try:
            t = next(self.tokens)
        except StopIteration:
            self.token = End()
        else:
            Token = dict(
                ID = Id,
                KEYWORD = Keyword,
                OPERATOR = Operator
            ).get(t.type, Literal)
            self.token = Token(t)

        return self

    def expression(self, rbp=0):
        t = self.token
        left = t.null(self.step())
        while rbp < self.token.lbp:
            t = self.token
            left = t.left(left, self.step())

        return left

def parse(tokens):
    return Parser(tokens).expression()
