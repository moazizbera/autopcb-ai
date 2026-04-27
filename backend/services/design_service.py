from __future__ import annotations

from backend.engine.solver import CircuitSolver, InsufficientVoltageError
from backend.models.circuit import Circuit
from backend.schemas.design_schema import DesignRequest


_COMPONENT_SOLVER_MAP: dict[str, str] = {
    "LED": "solve_led_circuit",
}


class UnsupportedComponentError(ValueError):
    """Raised when the service has no solver strategy for the requested component."""


class DesignService:
    def __init__(self, solver: CircuitSolver) -> None:
        self._solver = solver

    def generate_circuit(self, request: DesignRequest) -> Circuit:
        solver_method_name = _COMPONENT_SOLVER_MAP.get(request.target_component)
        if solver_method_name is None:
            raise UnsupportedComponentError(
                f"No circuit strategy available for component '{request.target_component}'"
            )

        solver_method = getattr(self._solver, solver_method_name)

        try:
            return solver_method(request.voltage)
        except InsufficientVoltageError:
            raise
