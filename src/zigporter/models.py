from datetime import datetime

from pydantic import BaseModel, Field


class AutomationRef(BaseModel):
    automation_id: str
    alias: str
    entity_references: list[str] = Field(default_factory=list)


class ZHAEntity(BaseModel):
    entity_id: str
    name: str
    name_by_user: str | None = None
    platform: str
    unique_id: str | None = None
    device_class: str | None = None
    disabled: bool = False
    state: str | None = None
    attributes: dict = Field(default_factory=dict)


class ZHADevice(BaseModel):
    device_id: str
    ieee: str
    name: str
    name_by_user: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    area_id: str | None = None
    area_name: str | None = None
    device_type: str
    quirk_applied: bool = False
    quirk_class: str | None = None
    entities: list[ZHAEntity] = Field(default_factory=list)
    automations: list[AutomationRef] = Field(default_factory=list)


class ZHAExport(BaseModel):
    exported_at: datetime
    ha_url: str
    devices: list[ZHADevice] = Field(default_factory=list)
