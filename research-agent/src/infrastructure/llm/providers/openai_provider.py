from typing import List, Dict, Tuple, Any

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from infrastructure.llm.providers.base import ChatProvider, EmbeddingProvider


class OpenAIChatProvider(ChatProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    # GPT 5 Implementation
    # --------------------
    # async def chat(self, messages: List[Dict[str, Any]], config: Dict) -> Tuple[str, int]:
    #     response = await self.client.responses.create(
    #         model=self.model,
    #         input=messages,
    #         # temperature=config.get("temperature", 0.7),
    #         # top_p=config.get("top_p", 0.95),
    #         max_output_tokens=config.get("max_tokens", 2048),
    #     )
    #
    #     return (
    #         response.output_text,
    #         response.usage.total_tokens if response.usage else 0,
    #     )

    async def chat(self, messages: List[ChatCompletionMessageParam], config: Dict) -> Tuple[str, int]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.get("temperature", 0.7),
            top_p=config.get("top_p", 0.95),
            max_tokens=config.get("max_tokens", 2048), )

        return (
            response.choices[0].message.content,
            response.usage.total_tokens if response.usage else 0,
        )


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def embed(self, text: str) -> List[float]:
        resp = await self.client.embeddings.create(model=self.model, input=text)
        return resp.data[0].embedding
