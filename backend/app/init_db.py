from app.core.database import engine, Base, SessionLocal
from app.models.models import HCP, Product

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(HCP).first():
        print("Database already seeded.")
        db.close()
        return

    # Seed HCPs
    hcps = [
        HCP(name="Dr. Smith", specialty="Cardiology"),
        HCP(name="Dr. John", specialty="Dermatology"),
        HCP(name="Dr. Emily", specialty="Pediatrics"),
        HCP(name="Dr. Sarah", specialty="Oncology"),
    ]
    
    # Seed Products
    products = [
        Product(name="Product X"),
        Product(name="Product Y"),
        Product(name="Product Z"),
    ]
    
    db.add_all(hcps)
    db.add_all(products)
    db.commit()
    db.close()
    print("Database initialized and seeded.")

if __name__ == "__main__":
    init_db()
