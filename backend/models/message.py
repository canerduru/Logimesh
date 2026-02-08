from enum import Enum
from typing import Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class MessageType(str, Enum):
    CAPACITY_OFFER = "CAPACITY_OFFER"
    LOAD_REQUEST = "LOAD_REQUEST"
    COUNTER_OFFER = "COUNTER_OFFER"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"

class BaseMessagePayload(BaseModel):
    pass

class CapacityOfferPayload(BaseMessagePayload):
    fleet_id: str
    vehicle_type: str
    capacity_tons: float
    current_location: Dict[str, float]  # {lat: float, lng: float}
    available_from: str
    status: str

class LoadRequestPayload(BaseMessagePayload):
    load_id: str
    origin: Dict[str, float]
    destination: Dict[str, float]
    weight_tons: float
    deadline: str
    price_offered: Optional[float] = None

class CounterOfferPayload(BaseMessagePayload):
    original_message_id: str
    price: float
    reason: Optional[str] = None

class AcceptPayload(BaseMessagePayload):
    original_message_id: str
    reason: Optional[str] = None

class RejectPayload(BaseMessagePayload):
    original_message_id: str
    reason: Optional[str] = None

class AgentMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: Optional[str] = None
    receiver_id: Optional[str] = None
    sender_agent_type: str
    receiver_agent_type: str
    message_type: MessageType
    payload: Dict[str, Any]
    conversation_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        use_enum_values = True
