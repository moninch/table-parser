from fastapi import APIRouter

from starlette.responses import JSONResponse


router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})
