from pygments.lexers.diff import DiffLexer
import pprint

lexer = DiffLexer()
tokens = list(lexer.get_tokens("+ added line" + " " * 10 + "\n"))
pprint.pprint(tokens)
