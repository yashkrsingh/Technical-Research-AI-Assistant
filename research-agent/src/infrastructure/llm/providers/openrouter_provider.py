from typing import List, Dict, Tuple

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from infrastructure.llm.providers.base import ChatProvider, EmbeddingProvider


class OpenRouterChatProvider(ChatProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def chat(self, messages: List[ChatCompletionMessageParam], config: Dict) -> Tuple[str, int]:
        pass


class OpenRouterEmbeddingProvider(EmbeddingProvider):

    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def embed(self, text: str) -> List[float]:
        pass