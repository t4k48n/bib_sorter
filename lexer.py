#!/usr/bin/enb python3

import re   # 正規表現

TEST_DATA = '''@article{ Rongrong1,
    author = "Rongrong Wang and Junmin Wang",
    title = "Fault-tolerant control with active fault diagnosis for four-wheel independently driven electric ground vehicles",
    journal = "IEEE Transactions on Vehicular Technology",
    volume = "60",
    number = "9",
    pages = "4276--4287",
    year = "2011",
    file = "./pdf/Rongrong2011FTCwithAFD.pdf"
}

@article{ Jiaxing2, 
    author = "Jiaxing Guo and Gang Tao and Yu Liu",
    title = "Adaptive actuator failure and structural damage compensation of NASA generic transport model",
    journal = "Journal of Dynamic Systems, Measurement, and Control",
    volume = "136",
    number = "3",
    pages = "1--10",
    year = "2014",
    file = "./pdf/Guo2014AdaptiveActFailComp_ofNASA_gen_trans.pdf"
}
'''

lbrace = re.compile(r'{')
rbrace = re.compile(r'}')
comma = re.compile(r',')
whites = re.compile(r'[ \n\r\t]*')
doctype = re.compile(r'@[a-z]+')
anychar = re.compile(r'.')
field = re.compile(r'([a-z]+)[ \t]*=[ \t]*"(.*?)"')
identifier = re.compile(r'[a-zA-Z0-9_\-]+')

LBrace = 'LBrace'
RBrace = 'RBrace'
Comma = 'Comma'
EOF = 'EOF'

class Doctype:
    def __init__(self, typename):
        self.typename = typename
    def __repr__(self):
        return 'Doctype({!r})'.format(self.typename)

class Identifier:
    def __init__(self, idname):
        self.idname = idname
    def __repr__(self):
        return 'Identifier({!r})'.format(self.idname)

class Field:
    def __init__(self, fname, value):
        self.fname = fname
        self.value = value
    def __repr__(self):
        return 'Field({!r}, {!r})'.format(self.fname, self.value)

class Invalid:
    def __init__(self, ch):
        self.ch = ch
    def __repr__(self):
        return 'Invalid({!r})'.format(self.ch)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0        # 読み取り位置

    def skip_whites(self):  # 空白文字（' ', '\n', '\r', '\t'）を読み飛ばす
        self.pos += re.match(whites, self.text[self.pos:]).end()

    def next_token(self):
        self.skip_whites()

        candidates = [
                # フィールド（ドキュメントプロパティ）
                (field, lambda r: Field(*r.groups())),
                # 左ブレース '{'
                (lbrace, lambda r: LBrace),
                # 右ブレース '}'
                (rbrace, lambda r: RBrace),
                # コンマ ','
                (comma, lambda r: Comma),
                # ドキュメントタイプ（e.g. @article and @book）
                (doctype, lambda r: Doctype(r.group()[1:])),
                # 識別名（e.g. '@article{'や'@block{'などの次に現れるドキュメントを同定するための記号）
                (identifier, lambda r: Identifier(r.group())),
                # 任意の1字（不正トークン）
                (anychar, lambda r: Invalid(r.group())),
                ]

        for pat, alloc in candidates:
            result = re.match(pat, self.text[self.pos:])
            if result:
                self.pos += result.end()
                return alloc(result)

        return EOF

minitest = '''@article{}
INVALID
@book{
    author = 	"Takatani Hideaki",
}
'''

lex = Lexer(minitest)
tk = lex.next_token()
while tk != EOF:
    print(tk)
    tk = lex.next_token()

print()

lex = Lexer(TEST_DATA)
tk = lex.next_token()
while tk != EOF:
    print(tk)
    tk = lex.next_token()
