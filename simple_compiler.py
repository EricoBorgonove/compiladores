import re

token_specification = [
    ('NUMBER', r'\d+'),    # token de numeros inteiros
    ('PLUS', r'\+'),       # token de soma
    ('MINUS', r'\-'),      # token de subtração
    ('MUL', r'\*'),        # token de multiplicação
    ('DIV', r'/'),         # token da divisão
    ('LPAREN', r'\()'),    # token parentese esquerdo
    ('RPAREN', r'\))'),    # token parentese direiro
    ('SKIP', r'[ \t]+'),   # ignora espaços em branco
    ('MISMATCH', '.')      # Qualquer outro caractere
]

token_re = '|'.join('?P<%s>%s'% pair for pair in token_specification)

def tokenize (code):
    tokens = []
    for match in re.finditer(token_re, code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'NUMBER':
            value = int (value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Caractere Inesperado: {value}')
        tokens.append((kind, value))
    return tokens

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right
        
class Number(ASTNode):
    def __init__ (self, value):
        self.value = value
        
class Parser:
    def __init__ (self, tokens):
        self.tokens = tokens
        self.pos =0
        
    def consume(self, expected_type = None):
        token_type, token_value = self.tokens[self.pos]
        if expected_type and token_type != expected_type:
            raise RuntimeError(f'Expected {expected_type} got {token_type}')
        self.pos += 1
        return token_value
    
    def parse(self):
        return self.expr()

def expr (self):
    node = self.term()
    while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
        op = self.consume()
        right = self.term()
        node = BinOp (node, op, right)
    return node

def term (self):
    node = self.factor()
    while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('MUL', 'DIV'):
        op = self.consume()
        right = self.factor()
        node = BinOp(node, op, right)
    return node

def factor (self):
    if self.tokens[self.pos][0] == 'NUMBER':
        return Number (self.consume('NUMBER'))
    elif self.tokens[self.pos][0] == 'LPAREN':
        self.consume('LPAREN')
        node = self.expor()
        self.consume('RPAREN')
        return node
    
    