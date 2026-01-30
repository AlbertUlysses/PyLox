from dataclasses import dataclass
from typing import Protocol

from lox_token import Token

class Expr(Protocol):
    def accept(self, visitor) -> str:
        ...


@dataclass
class Binary:
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor) -> str:
        return visitor.visit_binary_expr(self)

@dataclass
class Grouping:
    expression: Expr

    def accept(self, visitor) -> str:
        return visitor.visit_grouping_expr(self)

@dataclass
class Literal:
    value: object

    def accept(self, visitor) -> str:
        return visitor.visit_literal_expr(self)

@dataclass
class Unary:
    operator: Token
    right: Expr

    def accept(self, visitor) -> str:
        return visitor.visit_unary_expr(self)
