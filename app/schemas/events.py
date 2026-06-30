from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    deployment = "DEPLOYMENT"
    error = "ERROR"
    heartbeat = "HEARTBEAT"


class Environment(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"


class EventCreate(BaseModel):
    service_name: str = Field(min_length=1, max_length=120)
    event_type: EventType
    environment: Environment
    message: str = Field(min_length=1, max_length=1000)


class EventRead(EventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
