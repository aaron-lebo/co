import lexer
import parser

if __name__ == '__main__':
    print('co 0.1\n')

    while True:
        try:
            print(parser.parse(lexer.lex(input('co> '))))
        except NameError as e:
            print('error:', e)
