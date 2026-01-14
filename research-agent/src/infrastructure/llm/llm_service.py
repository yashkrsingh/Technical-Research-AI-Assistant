from typing import List, Dict

from infrastructure.llm.providers.base import ChatProvider, EmbeddingProvider


class LLMService:
    def __init__(self, chat_provider: ChatProvider, embedding_provider: EmbeddingProvider):
        self.chat_provider = chat_provider
        self.embedding_provider = embedding_provider

        self.default_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 2048,
        }

    def set_model(self, model: str):
        if hasattr(self.chat_provider, "set_model"):
            self.chat_provider.set_model(model)
        else:
            raise RuntimeError("This provider does not support model switching")

    async def chat(self, messages: List[Dict], config: dict | None = None):
        cfg = {**self.default_config, **(config or {})}
        return await self.chat_provider.chat(messages, cfg)

    async def embed(self, text: str):
        return await self.embedding_provider.embed(text)

