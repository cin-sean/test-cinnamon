from fastapi import FastAPI
from .routers import test, operations

app = FastAPI()
app.include_router(test.router)
app.include_router(operations.router)
