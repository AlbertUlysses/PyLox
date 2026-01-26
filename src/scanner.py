from dataclasses import dataclass, field

from lox_token import Token
from token_type import TokenType

from report_error import report_error

@dataclass
class Scanner:
    source: str
    start: int = 0
    current: int = 0
    line: int = 1
    has_error: bool = False
    tokens: list[Token] = field(default_factory=list)
    keywords: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.keywords = {
            "and" : TokenType.AND,
            "class" : TokenType.CLASS,
            "else" : TokenType.ELSE,
            "false" : TokenType.FALSE,
            "for" : TokenType.FOR,
            "fun" : TokenType.FUN,
            "if" : TokenType.IF,
            "nil" : TokenType.NIL,
            "or" : TokenType.OR,
            "print" : TokenType.PRINT,
            "return" : TokenType.RETURN,
            "super" : TokenType.SUPER,
            "this" : TokenType.THIS,
            "true" : TokenType.TRUE,
            "var" : TokenType.VAR,
            "while" : TokenType.WHILE
        }

    def scan_tokens(self)->list[Token]:
        while not self.is_at_end:
            self.start = self.current
            self.scan_token(self.source[self.current])
            if not self.is_at_end:
                self.advance()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self, c: str) -> None:
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS);
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG);
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL);
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS);
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER);
            case '/':
                if self.match('/'):
                    while ((self.peek != '\n') & (not self.is_at_end)):
                        self.advance
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number
                elif self.is_alpha(c):
                    self.identifier
                else:
                    report_error(self.line, "", "Unexpected Character.")
                    self.has_error = True

    def is_digit(self, c: str) -> bool:
        return (c >= '0') & (c <= '9')

    def is_alpha(self,c: str) -> bool:
        return (
            ((c>='a') & (c <='z')) |
            ((c>='A') & (c <='Z')) |
            (c == '_')
        )
    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) | self.is_digit(c)

    def string(self) -> None:
        while (self.peek != '"') & (not self.is_at_end):
            if self.peek == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end:
            report_error(self.line, "", "Unterminated String.")
        else:
            self.advance() # account for the next letter
            self.current += 1 #account for the quote
            value = self.source[self.start:self.current]
            self.add_token(TokenType.STRING, value.strip('"'))

    def advance(self) -> str:
        #if not self.is_at_end:
        self.current += 1
        return self.source[self.current]

    def add_token(self, type: TokenType, literal: object = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end:
            return False
        if self.source[self.current+1] != expected:
            return False
        self.current += 1
        return True

    @property
    def identifier(self) -> None:
        """..."""
        #while (self.is_alpha_numeric(self.peek)):
        while self.is_alpha_numeric(self.source[self.current]):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, None)
        if not token_type:
            token_type = TokenType.IDENTIFIER 
        self.add_token(token_type)

    @property
    def number(self) -> None:
        while self.is_digit(self.peek):
            self.advance()
        if self.peek == '.' & self.is_digit(self.peek_next):
            self.advance()
            while self.is_digit(self.peek):
                self.advance()
        self.add_token(
            TokenType.NUMBER, eval(self.source[self.start, self.current])
        )

    @property
    def peek(self) -> str:
        if self.is_at_end:
            return '\0'
        else:
            return self.source[self.current+1]
    @property
    def peek_next(self) -> str:
        if self.current + 1  >= (len(self.source)-1):
            return '\0'
        return self.source[self.current+1]

    @property
    def is_at_end(self) -> bool:
        return self.current >= (len(self.source)-1)
