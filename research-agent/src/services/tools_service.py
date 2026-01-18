from typing import List, Dict, Any

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


    async def research_planner(self, sub_task_list: str):
        logger.info("Researching topics")

        output = await self.llm_service.make_llm_call(system_prompt="",
                                                      user_prompt=OrchestratorPrompts.RESEARCH_PLANNER_USER_PROMPT
                                                      .substitute(sub_task_list=sub_task_list)
                                                      )

        response = output.get("response")
        tokens_used = output.get("tokens")

        return response, tokens_used

    async def research_executor(self, research_topics: List[str]):
        logger.info("Researching citations and relevant docs")

        docs = []
        citations = []

        for query in research_topics:
            results = await self.search_web(query)
            for r in results:
                docs.append({
                    "content": r["snippet"],
                    "source": r["url"]
                })
                citations.append(r["url"])

        return {
            "retrieved_docs": docs,
            "citations": list(set(citations))
        }


    async def approach_comparator(self, research_topics: List[str], relevant_docs: List[Dict[str, Any]]):
        logger.info("Comparing approaches")

        output = await self.llm_service.make_llm_call(system_prompt="",
                                                      user_prompt=OrchestratorPrompts.APPROACH_COMPARATOR_SYSTEM_PROMPT
                                                      .substitute(research_topics=research_topics,
                                                                  relevant_docs=relevant_docs)
                                                      )

        response = output.get("response")
        tokens_used = output.get("tokens")

        return response, tokens_used


    async def solution_synthesizer(self, approaches: List[Dict[str, Any]]):
        logger.info("Synthesizing solution and reasoning behind selection of an approach")

        output = await self.llm_service.make_llm_call(system_prompt="",
                                                      user_prompt=OrchestratorPrompts.SOLUTION_SYNTHESIZER_PROMPT
                                                      .substitute(approaches=approaches)
                                                      )

        response = output.get("response")
        tokens_used = output.get("tokens")

        return response, tokens_used


    async def structured_plan_generator(self, selected_approach: Dict[str, Any]):
        logger.info("Synthesizing solution")

        output = await self.llm_service.make_llm_call(system_prompt="",
                                                      user_prompt=OrchestratorPrompts.STRUCTURED_PLAN_GENERATOR_PROMPT
                                                      .substitute(selected_approach=selected_approach)
                                                      )

        response = output.get("response")
        tokens_used = output.get("tokens")

        return response, tokens_used


    # -----------------------------
    # HELPER METHODS
    # _____________________________


    async def search_web(self, query: str):
        pass



