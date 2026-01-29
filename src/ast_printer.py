from dataclasses import dataclass

@dataclass
class ASTPrinter:

    def print_ast(self, expr: Expr) -> str:
        match expr.__doc__[:ending_int]:
            case 'Binary':
                return self.visit_binary_expr()

    def visit_binary_expr(self) -> str:
        ...

def main()->None:
    expression = Binary()
    print(ASTPrint().print(expression)

