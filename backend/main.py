from fastapi import FastAPI
from  core.settings import settings
from db.base import Base
from db.session import engine

# Import all the models so that they are registered with SQLAlchemy
from apps.auth import models as auth_models

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Create the database tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Define a simple root endpoint
@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME} API!"}