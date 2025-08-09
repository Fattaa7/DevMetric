from fastapi import FastAPI
from app.api import user_routes, auth_routes, metric_routes, admin_routes
from app.core.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(metric_routes.router)
app.include_router(admin_routes.router)