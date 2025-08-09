from fastapi import FastAPI
from app.api import user_routes, auth_routes, metric_routes, admin_routes
from app.core.database import Base, engine
import os


user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"


# Initialize the database connection
# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(metric_routes.router)
app.include_router(admin_routes.router)