from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Fleet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_id: str
    vehicle_type: str
    capacity_tons: float
    current_location_lat: float
    current_location_lng: float
    status: str = "IDLE"
    available_from: datetime = Field(default_factory=datetime.now)

class Load(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_id: str
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float
    weight_tons: float
    deadline: datetime
    status: str = "PENDING"
    price_offered: Optional[float] = None

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    load_id: str
    fleet_id: str
    amount: float
    carrier_company_id: str
    shipper_company_id: str
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.now)
    finalized_at: Optional[datetime] = None
