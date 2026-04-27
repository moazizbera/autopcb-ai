from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Sequence


class ComponentType(StrEnum):
    RESISTOR = "resistor"
    LED = "led"
    CAPACITOR = "capacitor"
    DIODE = "diode"


@dataclass(frozen=True)
class Component:
    component_id: str
    component_type: ComponentType
    label: str
    value: float
    unit: str

    def __str__(self) -> str:
        return f"{self.label} ({self.value} {self.unit})"


@dataclass(frozen=True)
class Connection:
    source_id: str
    target_id: str


@dataclass
class Circuit:
    supply_voltage: float
    components: list[Component] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def get_component_by_type(self, component_type: ComponentType) -> Sequence[Component]:
        return [c for c in self.components if c.component_type == component_type]
