from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.engine.solver import CircuitSolver, InsufficientVoltageError
from backend.models.circuit import Circuit
from backend.schemas.design_schema import (
    ComponentSchema,
    ConnectionSchema,
    DesignRequest,
    DesignResponse,
)
from backend.services.design_service import DesignService, UnsupportedComponentError


router = APIRouter(prefix="/api/v1/design", tags=["design"])


def _get_design_service() -> DesignService:
    return DesignService(solver=CircuitSolver())


def _circuit_to_response(circuit: Circuit) -> DesignResponse:
    return DesignResponse(
        supply_voltage=circuit.supply_voltage,
        components=[
            ComponentSchema(
                component_id=c.component_id,
                component_type=c.component_type,
                label=c.label,
                value=c.value,
                unit=c.unit,
            )
            for c in circuit.components
        ],
        connections=[
            ConnectionSchema(source_id=conn.source_id, target_id=conn.target_id)
            for conn in circuit.connections
        ],
    )


@router.post(
    "/generate",
    response_model=DesignResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a circuit design from supply voltage and target component",
)
def generate_circuit_design(
    request: DesignRequest,
    service: DesignService = Depends(_get_design_service),
) -> DesignResponse:
    try:
        circuit = service.generate_circuit(request)
    except InsufficientVoltageError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except UnsupportedComponentError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return _circuit_to_response(circuit)
