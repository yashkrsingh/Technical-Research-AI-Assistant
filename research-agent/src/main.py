import asyncio
import logging
import os
import sys

import api
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn import Config, Server

from config.settings import configuration
from exceptions.app_exceptions import AppErrorCodes
from exceptions.app_exceptions import (ResultValidationException, InternalServerError, AppException, )


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

logger.remove()
logger.add(sys.stderr, level=configuration.api.log_level, backtrace=True, diagnose=False)

app = api.create_app()


@app.exception_handler(ResultValidationException)
async def result_validation_exception_handler(request: Request, exc: ResultValidationException):
    return JSONResponse(status_code=int(AppErrorCodes.VALIDATION_ERROR[0]),
                        content={
                            "status_code": AppErrorCodes.VALIDATION_ERROR[0],
                            "message": str(exc),
                            "details": exc.details,
                        })


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return JSONResponse(status_code=int(AppErrorCodes.INTERNAL_SERVER_ERROR[0]),
                        content={
                            "status_code": AppErrorCodes.INTERNAL_SERVER_ERROR[0],
                            "message": str(exc),
                            "details": exc.details,
                        })


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=int(AppErrorCodes.INTERNAL_SERVER_ERROR[0]),
                        content={
                            "status_code": AppErrorCodes.INTERNAL_SERVER_ERROR[0],
                            "message": str(exc),
                            "details": exc.details,
                        })


async def run_api():
    host = configuration.api.host
    is_windows = os.name == "nt"
    port = configuration.api.port or (5000 if is_windows else 8000)
    logger.info(f"Starting Uvicorn server on {host}:{port}")
    server = Server(Config(app=app,
                           host=host,
                           port=port,
                           log_level=configuration.api.log_level.lower(),
                           log_config=None,
                           ))
    await server.serve()


async def main():
    if configuration.app_mode == "api":
        await run_api()


if __name__ == "__main__":
    asyncio.run(main())
