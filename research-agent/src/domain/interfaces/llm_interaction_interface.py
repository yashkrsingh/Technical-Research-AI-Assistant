from abc import abstractmethod, ABC
from typing import Optional, Any, Dict


class LlmInteractionInterface(ABC):

    @abstractmethod
    async def make_llm_call(self,
                            system_prompt: Optional[str],
                            user_prompt: str,
                            model: Optional[str] = None,
                            message_type: str = "text",
                            media_base64: Optional[str] = None, ) -> Dict:
        pass

    @abstractmethod
    async def get_embedding(self, text: str):
        pass
