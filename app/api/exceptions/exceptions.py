from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request

def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.status_code,
            "error_message": exc.detail,
        },
    )