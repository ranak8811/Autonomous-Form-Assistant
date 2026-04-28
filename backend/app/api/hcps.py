from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import HCP
from app.schemas.schemas import HCP as HCPSchema

router = APIRouter(prefix="/hcps", tags=["HCPs"])

@router.get("/", response_model=List[HCPSchema])
def get_hcps(db: Session = Depends(get_db)):
    """Fetches all Healthcare Professionals from the database."""
    return db.query(HCP).all()
