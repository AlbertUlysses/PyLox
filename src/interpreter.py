from dataclasses import dataclass

from report_error import LoxRuntimeError
from expr import Expr, Binary, Grouping, Literal, Unary
from lox_token import Token

@dataclass
class Interpeter:

    def visit_literal_expr(self, expr: Expr) -> object:
        return expr.value

    def visit_grouping_expr(self, expr: Expr) -> object:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Expr) -> object:
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right))
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -(float(right))
            case _:
                return None
    def visit_binary_expr(self, expr: Expr) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left,right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left,right)
                return left >=right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left,right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left,right)
                return left <=right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left,right)
                return float(left) - float(right)
            case TokenType.Plus:
                if (isinstance(left,(int, float)) & isinstance(right,(int, float))):
                    return left + right
                if (isinstance(left,str) & isinstance(right,str)):
                    return left + right
                return None
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left,right)
                return float(left)/float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left,right)
                return float(left) * float(right)
            case _:
                return None

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(this)

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, (int, float)):
            return None
        raise LoxRuntimeError(f"Operator: {Operator.type}. Operand must be a number.")

    def check_number_operands(self, operator: Token, left: object, right: object) -> None:
        if (isinstance(left, (int, float)) & isinstance(right, (int, float)):
            return None
        raise LoxRuntimeError(f"Operator: {Operator.type}. Operand must be a number.")

    def is_truthy(self, exp_object: object) -> bool:
        if expr_object is None:
            return False
        if type(expr_object) == bool:
            return expr_object
        return True

    def is_equal(self, a: object, b: object) -> bool:
        if ((a is None) & (b is None)):
            return True
        if ((a is None) | (b is None)):
            return False 
        return a == b
