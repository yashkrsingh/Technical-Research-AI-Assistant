from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class ChatProvider(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict], config: Dict) -> Tuple[str, int]:
        """Execute a chat completion and return (text, tokens)."""
        pass


class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        pass
