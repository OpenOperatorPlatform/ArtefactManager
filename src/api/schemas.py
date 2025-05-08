from typing import Optional

from pydantic import BaseModel, Field


class PostArtefactExists(BaseModel):
    registry_url: str = Field(
        ...,
        description="Container registry URL including project",
        json_schema_extra={"example": "https://registry.example.com/project-name"},
    )
    registry_username: Optional[str] = Field(
        default=None,
        description="Optional username for authentication",
        json_schema_extra={"example": "admin"},
    )
    registry_password: Optional[str] = Field(
        default=None,
        description="Optional password for authentication",
        json_schema_extra={"example": "password"},
    )
    artefact_name: str = Field(
        ...,
        description="Artefact name within the project",
        json_schema_extra={"example": "nginx"},
    )
    artefact_tag: str = Field(
        ...,
        description="Artefact tag to check",
        json_schema_extra={"example": "latest"},
    )


class PostArtefactExistsResponse(BaseModel):
    exists: bool


class PostCopyArtefact(BaseModel):
    src_registry_url: str = Field(
        ...,
        description="Source container registry URL including project",
        json_schema_extra={"example": "https://registry.example.com/project-name"},
    )
    src_registry_username: Optional[str] = Field(
        default=None,
        description="Optional username for source registry authentication",
        json_schema_extra={"example": "admin"},
    )
    src_registry_password: Optional[str] = Field(
        default=None,
        description="Optional password for source registry authentication",
        json_schema_extra={"example": "password"},
    )
    src_artefact_name: str = Field(
        ..., description="Source artefact name", json_schema_extra={"example": "nginx"}
    )
    src_artefact_tag: str = Field(
        ..., description="Source artefact tag", json_schema_extra={"example": "latest"}
    )
    dst_registry_url: str = Field(
        ...,
        description="Destination container registry URL including project",
        json_schema_extra={
            "example": "https://another.registry.example.com/project-name"
        },
    )
    dst_registry_username: Optional[str] = Field(
        default=None,
        description="Optional username for dst registry authentication",
        json_schema_extra={"example": "admin"},
    )
    dst_registry_password: Optional[str] = Field(
        default=None,
        description="Optional password for dst registry authentication",
        json_schema_extra={"example": "password"},
    )
    dst_artefact_name: Optional[str] = Field(
        default=None,
        description="Destination artefact name",
        json_schema_extra={"example": "nginx"},
    )
    dst_artefact_tag: Optional[str] = Field(
        default=None,
        description="Destination artefact tag",
        json_schema_extra={"example": "latest"},
    )


class PostCopyArtefactResponse(BaseModel):
    success: bool
