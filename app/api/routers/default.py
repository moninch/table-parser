import logging
from fastapi import APIRouter, BackgroundTasks

from starlette.responses import JSONResponse


router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})
