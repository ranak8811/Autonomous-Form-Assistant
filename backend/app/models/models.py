from sqlalchemy import Column, Integer, String, Date, Time, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class HCP(Base):
    __tablename__ = "hcps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    interaction_type = Column(String) # Meeting, Call, etc.
    date = Column(Date)
    time = Column(Time)
    attendees = Column(JSON) # List of names
    topics_discussed = Column(Text)
    materials_shared = Column(JSON) # List of strings
    samples_distributed = Column(JSON) # List of strings
    sentiment = Column(String) # Positive, Neutral, Negative
    outcomes = Column(Text)
    follow_up_actions = Column(Text)
    
    hcp = relationship("HCP")
