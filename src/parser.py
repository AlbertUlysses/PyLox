from dataclasses import dataclass

from expr import Expr, Binary, Unary, Grouping, Literal
from lox_token import Token
from token_type import TokenType
from report_error import report_error, ParserError


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right);

        return expr

    def match(self, types: TokenType)->bool:
        for token_type in types:
            if(self.check(token_type)):
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
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)
        if self.match([TokenType.NIL]):
            return Literal(None)
        if self.match([TokenType.NUMBER,TokenType.STRING]):
            return Literal(self.previous().literal)
        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after exprssion.")
            return Groupinng(expr)
        self.error(self.peek(), "expect Expresion.")

    def consume(self, lox_type: TokenType, message: str) -> Token:
        if self.check(lox_type):
            return self.advance()
        # this part below I need to focus on second round
        self.error(self.peek(), meesage)

    def error(self, token: Token, message: str) -> None:
        report_error(token.line, f"Parser error: {token.type.name}",message)
        raise ParserError()

    def synchronize(self) -> None:
        self.advance()
        while (not self.is_at_end()):
            if self.previous().type == TokenType.SEMICOLON:
                return None
            match self.peek().type:
                case (
                    TokenType.CLASS | TokenType.FUN | TokenType.VAR | TokenType.FOR |
                    TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN):
                    return None
        advance()

    def parse(self) -> Expr:
        try:
            return self.expression()
        except ParserError:
            return None
