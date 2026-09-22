from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Line:
    name: str
    unit_price: Decimal
    quantity: int


@dataclass
class Cart:
    lines: dict[str, Line] = field(default_factory=dict)

    def add(self, name: str, unit_price: Decimal, quantity: int) -> None:
        line = self.lines.get(name)
        if line is None:
            self.lines[name] = Line(name, unit_price, quantity)
        else:
            line.quantity += quantity

    def quantity_of(self, name: str) -> int:
        line = self.lines.get(name)
        return line.quantity if line else 0

    def total(self) -> Decimal:
        return sum((l.unit_price * l.quantity for l in self.lines.values()), Decimal("0.00"))
