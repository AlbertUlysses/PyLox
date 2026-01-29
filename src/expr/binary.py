from dataclasses import dataclass

@dataclass
class Binary:
    left: expr
    operator: token
    right: expr

    def accept(self, vistor):
        return visitor.visit_binary_expr()
