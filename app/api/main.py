from fastapi import FastAPI

from app.api.routers import operations, test

app = FastAPI()
app.include_router(test.router)
app.include_router(operations.router)
