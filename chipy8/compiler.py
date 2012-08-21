# coding: utf-8

from analyzer import analyse

chip8_tokens = [
    dict(type='T_INSTRUCTION', regex=r'^(RCA|DRW|LD|CALL|DT|SE|JP)\s', store=True),    
    dict(type='T_ADDRESS', regex=r'\$([\dA-F]{2,4})', store=True),
    dict(type='T_HEX_NUMBER', regex=r'\#\$?([\dA-F]{2})', store=True), #TODO: change to HEX_NUMBER
    dict(type='T_LABEL', regex=r'^([a-zA-Z][_a-zA-Z\d]{1,})\:', store=True),
    dict(type='T_MARKER', regex=r'^[a-zA-Z][_a-zA-Z\d]{1,}', store=True),
    dict(type='T_STRING', regex=r'^"[^"]*"', store=True),
    dict(type='T_INDEX_REGISTER', regex=r'^(I)[\s,\]]', store=True),
    dict(type='T_BDC_REGISTER', regex=r'^(B)[\s,]', store=True),
    dict(type='T_F_REGISTER', regex=r'^(F)[\s,]', store=True),
    dict(type='T_REGISTER', regex=r'^(V([\dA-F]))', store=True),
    dict(type='T_SEPARATOR', regex=r'^,', store=True),
    dict(type='T_OPEN', regex=r'^\(', store=True),
    dict(type='T_CLOSE', regex=r'^\)', store=True),
    dict(type='T_OPEN_SQUARE_BRACKETS', regex=r'^\[', store=True),
    dict(type='T_CLOSE_SQUARE_BRACKETS', regex=r'^\]', store=True),
    dict(type='T_DECIMAL_ARGUMENT', regex=r'^[\d]+', store=True),
    dict(type='T_ENDLINE', regex=r'^\n', store=True),
    dict(type='T_WHITESPACE', regex=r'^[ \t\r]+', store=False),
    dict(type='T_COMMENT', regex=r'^;[^\n]*', store=False)
]

def lexical(code):
    return analyse(code, chip8_tokens)