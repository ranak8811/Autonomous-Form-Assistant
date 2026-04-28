from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Product
from app.schemas.schemas import Product as ProductSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    """Fetches all Products from the database."""
    return db.query(Product).all()
