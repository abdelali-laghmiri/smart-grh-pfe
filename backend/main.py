from fastapi import FastAPI
from  core.settings import settings
from db.base import Base
from db.session import engine


# Import all the models so that they are registered with SQLAlchemy
from apps.auth import models as auth_models
#Import all roters 
from apps.auth.routers import router as auth_routers
from apps.organization.routers import router as orga_routers

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

#inclouding 
app.include_router(auth_routers)
app.include_router(orga_routers)
# Create the database tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Define a simple root endpoint
@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME} API!"}