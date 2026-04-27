from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


SUPPORTED_COMPONENTS = {"LED"}


class DesignRequest(BaseModel):
    voltage: float = Field(..., gt=0.0, le=50.0, description="Supply voltage in volts")
    target_component: str = Field(..., min_length=1, description="Target component type (e.g. 'LED')")

    @field_validator("target_component")
    @classmethod
    def validate_target_component(cls, value: str) -> str:
        normalised = value.strip().upper()
        if normalised not in SUPPORTED_COMPONENTS:
            raise ValueError(
                f"Unsupported target component '{value}'. Supported: {sorted(SUPPORTED_COMPONENTS)}"
            )
        return normalised


class ComponentSchema(BaseModel):
    component_id: str
    component_type: str
    label: str
    value: float
    unit: str


class ConnectionSchema(BaseModel):
    source_id: str
    target_id: str


class DesignResponse(BaseModel):
    supply_voltage: float
    components: list[ComponentSchema]
    connections: list[ConnectionSchema]
