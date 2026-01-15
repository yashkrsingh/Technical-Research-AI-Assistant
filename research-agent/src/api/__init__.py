from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from api.controllers import agent_controller, db_controller
from config.settings import configuration
from infrastructure.database.database_engine import DatabaseEngine
from infrastructure.llm.bootstrap import LLMApplicationBootstrap


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Tech Research Agent API...")

    try:
        engine = DatabaseEngine.get_engine()
        logger.info("Database connection established")

        llm_service = LLMApplicationBootstrap.build_llm_interaction_service()
        app.state.llm_service = llm_service
        logger.info("LLM service initialized")
    except Exception as e:
        logger.exception("Failed to initialize database connection")
        raise e

    yield

    logger.info("Shutting down Tech Research Agent API...")
    await engine.dispose()
    logger.info("Database connections closed")

def create_app():
    application = FastAPI(
        title="Tech Research Agent API",
        version="0.0.1",
        description="APIs for Tech Research Agent",
        openapi_url="/api/openapi.json",
        docs_url="/",
        lifespan=lifespan,
        swagger_ui_init_oauth={
            "clientId": "swagger-ui",
            "appName": "Tech Research Agent API",
            "usePkceWithAuthorizationCodeGrant": True,
        },
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(agent_controller.agent_api_router)
    if configuration.local:
        application.include_router(db_controller.db_router)
    logger.info("API routers registered")

    return application
