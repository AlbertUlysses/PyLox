from dataclasses import dataclass

from expr import Expr, Binary
from lox_token import Token
from token_type import TokenType

@dataclass
class Parser:
    tokens: list[Token]
    curent: int = 0

    def expresion(self) ->:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right);

        return expr

    def match(types: TokenType)->bool:
        for token_type in types:
            if(check(token_type)):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type==token_type

    def advance(self) -> Token:
        if (not self.is_at_end()):
            self.current+=1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def comparison(self) -> Expr:
        expr = self.term()
        while match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

