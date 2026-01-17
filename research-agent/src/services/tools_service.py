from loguru import logger

from domain.interfaces.llm_interaction_interface import LlmInteractionInterface
from domain.interfaces.tools_interface import ToolsInterface
from domain.prompts.orchestrator_prompts import OrchestratorPrompts


class ToolsService(ToolsInterface):

    def __init__(self, llm_service: LlmInteractionInterface):
        self.llm_service = llm_service

    async def decompose_tasks(self, user_query: str):
        logger.info("Starting to get task list")

        output = await self.llm_service.make_llm_call(system_prompt="",
                                                      user_prompt=OrchestratorPrompts.TASK_DECOMPOSER_USER_PROMPT
                                                      .substitute(user_query=user_query)
                                                      )

        response = output.get("response")
        tokens_used = output.get("tokens")

        return response, tokens_used


    async def decompose_tasks(self, user_query: str):
        logger.info("Starting to get task list")

        output = await self.llm_service.make_llm_call(system_prompt="",
                                                      user_prompt=OrchestratorPrompts.TASK_DECOMPOSER_USER_PROMPT
                                                      .substitute(user_query=user_query)
                                                      )

        response = output.get("response")
        tokens_used = output.get("tokens")

        return response, tokens_used



