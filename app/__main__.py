import asyncio
import logging
from fastapi import BackgroundTasks
import pandas as pd
import uvicorn

# import app.loggers.logger as logger

# from aiohttp import web
# from aiogram import Bot, Dispatcher
# from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.settings import SETTINGS

# from app.utils.mongodb import MongoDB
# from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    uvicorn.run(
        app="app.api.server:app",
        host=SETTINGS.API_HOST,
        port=SETTINGS.API_PORT,
        log_level=SETTINGS.LOGGING_LEVEL.lower(),
        reload=True,
        reload_includes=["app"],
    )


if __name__ == "__main__":
    logging.warning("Starting bot")
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
    logging.warning("Bot stopped")
