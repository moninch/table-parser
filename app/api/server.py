from fastapi import FastAPI
from app.api.routers.parser import router as parser_router
from app.api.routers.default import router as default_router

app = FastAPI()
app.include_router(parser_router)
app.include_router(default_router)
