from enum import Enum

from pydantic import field_validator, model_validator
from sqlmodel import Field, SQLModel


class ItemStatus(str, Enum):
    LOST = "Lost"
    FOUND = "Found"
    RETURNED = "Returned"


def _clean_text(value: object) -> object:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("This field must not be empty or whitespace-only")
    return value.strip()


class ItemBase(SQLModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=3)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: ItemStatus

    @field_validator("title", "description", "category", "location", "reported_by", mode="before")
    @classmethod
    def validate_text_fields(cls, value: object) -> object:
        return _clean_text(value)


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=3)
    category: str | None = Field(default=None, min_length=1)
    location: str | None = Field(default=None, min_length=1)
    reported_by: str | None = Field(default=None, min_length=1)
    status: ItemStatus | None = None

    @field_validator("title", "description", "category", "location", "reported_by", mode="before")
    @classmethod
    def validate_text_fields(cls, value: object) -> object:
        return _clean_text(value)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value: object) -> object:
        if value is None:
            raise ValueError("Status must be Lost, Found, or Returned")
        return value

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "ItemUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self


class ItemRead(ItemBase):
    id: int


class MessageResponse(SQLModel):
    message: str