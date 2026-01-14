from infrastructure.llm.providers.openai_provider import OpenAIChatProvider, OpenAIEmbeddingProvider


class ProviderFactory:
    """
    Responsible for creating concrete LLM providers.
    Choose which vendor llm is to be used
    """

    @staticmethod
    def create(provider: str, api_key: str, model: str, embedding_model: str):
        if provider == "openai":
            return (
                OpenAIChatProvider(api_key=api_key, model=model),
                OpenAIEmbeddingProvider(api_key=api_key, model=embedding_model),
            )

        raise ValueError(f"Unsupported LLM provider: {provider}")
