from domain.interfaces.llm_interaction_interface import LlmInteractionInterface
from infrastructure.llm.llm_service import LLMService
from config.settings import configuration
from infrastructure.llm.providers.provider_factory import ProviderFactory
from services.llm_interaction_service import LlmInteractionService


class LLMApplicationBootstrap:
    """
    Wires together providers and services.
    This is the single entry point for LLM setup.
    """

    @staticmethod
    def build_llm_interaction_service() -> LlmInteractionInterface:
        chat_provider, embedding_provider = ProviderFactory.create(
            provider=configuration.llm.llm_provider,
            api_key=configuration.llm.llm_api_key,
            model=configuration.llm.llm_model,
            embedding_model=configuration.llm.llm_embedding_model,
        )

        llm_service = LLMService(
            chat_provider=chat_provider,
            embedding_provider=embedding_provider,
        )

        return LlmInteractionService(llm_service)
