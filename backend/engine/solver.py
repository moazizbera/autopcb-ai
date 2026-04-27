from __future__ import annotations

import uuid

from backend.models.circuit import Circuit, Component, ComponentType, Connection


# Standard LED electrical characteristics (per JEDEC-style specs)
_LED_FORWARD_VOLTAGE_V: float = 2.0
_LED_OPERATING_CURRENT_A: float = 0.020  # 20 mA


class InsufficientVoltageError(ValueError):
    """Raised when supply voltage cannot drive the target circuit safely."""


class CircuitSolver:
    """Stateless solver that constructs a safe circuit for a given supply voltage and target component."""

    def solve_led_circuit(self, supply_voltage: float) -> Circuit:
        self._assert_voltage_sufficient(supply_voltage)

        resistor = self._compute_current_limiting_resistor(supply_voltage)
        led = self._make_led_component()
        circuit = Circuit(supply_voltage=supply_voltage)

        circuit.add_component(resistor)
        circuit.add_component(led)
        circuit.add_connection(Connection(source_id="VCC", target_id=resistor.component_id))
        circuit.add_connection(Connection(source_id=resistor.component_id, target_id=led.component_id))
        circuit.add_connection(Connection(source_id=led.component_id, target_id="GND"))

        return circuit

    def _assert_voltage_sufficient(self, supply_voltage: float) -> None:
        if supply_voltage <= _LED_FORWARD_VOLTAGE_V:
            raise InsufficientVoltageError(
                f"Supply voltage {supply_voltage}V is insufficient to drive an LED "
                f"(minimum required: >{_LED_FORWARD_VOLTAGE_V}V)"
            )

    def _compute_current_limiting_resistor(self, supply_voltage: float) -> Component:
        voltage_drop = supply_voltage - _LED_FORWARD_VOLTAGE_V
        resistance_ohms = round(voltage_drop / _LED_OPERATING_CURRENT_A, 2)

        return Component(
            component_id=f"R_{uuid.uuid4().hex[:8]}",
            component_type=ComponentType.RESISTOR,
            label="R1",
            value=resistance_ohms,
            unit="Ω",
        )

    def _make_led_component(self) -> Component:
        return Component(
            component_id=f"LED_{uuid.uuid4().hex[:8]}",
            component_type=ComponentType.LED,
            label="D1",
            value=_LED_FORWARD_VOLTAGE_V,
            unit="V",
        )
