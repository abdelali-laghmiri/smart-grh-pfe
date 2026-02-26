from fastapi import FastAPI
from  core.settings import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME} API!"}