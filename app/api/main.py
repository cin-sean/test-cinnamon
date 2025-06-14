from fastapi import FastAPI, HTTPException

from app.api.exceptions.exceptions import custom_http_exception_handler
from app.api.routers import files, tasks
from app.shared.db.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

app.add_exception_handler(HTTPException, custom_http_exception_handler)
