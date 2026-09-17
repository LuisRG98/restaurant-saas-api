from app.core.database import engine, Base
from app.models.restaurant import Restaurant


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")