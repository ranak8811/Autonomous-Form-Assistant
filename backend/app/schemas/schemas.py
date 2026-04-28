from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

class HCPBase(BaseModel):
    name: str
    specialty: str

class HCPCreate(HCPBase):
    pass

class HCP(HCPBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    hcp_id: int
    interaction_type: str
    date: date
    time: time
    attendees: List[str]
    topics_discussed: str
    materials_shared: List[str]
    samples_distributed: List[str]
    sentiment: str
    outcomes: str
    follow_up_actions: str

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    class Config:
        from_attributes = True
