from dataclasses import dataclass

from expr import Binary, Grouping, Literal, Unary, Expr
from lox_token import Token
from token_type import TokenType

@dataclass
class ASTPrinter:

    def print_ast(self, expr: Expr) -> str:
        ending_int = expr.__doc__.find('(')
        match expr.__doc__[:ending_int]:
            case 'Binary':
                return self.visit_binary_expr(expr)
            case 'Grouping':
                return self.visit_grouping_expr(expr)
            case 'Literal':
                return self.visit_literal_expr(expr)
            case 'Unary':
                return self.visit_unary_expr(expr)
            case _:
                pass

    def parenthesize(self, name: str, exprs_values: list[str]) -> str:
        return " ".join(["("] + [name] + [str(expr.accept(self)) for expr in exprs_values]+[")"])

    def visit_binary_expr(self, expr: Expr) -> str:
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr: Expr) -> str:
        return self.parenthesize("group", [expr.expression])

    def visit_literal_expr(self, expr: Expr) -> str:
        return "nil" if expr.value is None else expr.value

    def visit_unary_expr(self, expr: Expr) -> str:
        return self.parenthesize(expr.operator.lexeme, [expr.right])

def main()->None:
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )
    print(ASTPrinter().print_ast(expression))

if __name__=="__main__":
    main()
