from typing import Dict, Optional, Any, Tuple

from loguru import logger
from openai import AsyncOpenAI


class LLMService:
    """
    Async service using the OpenAI SDK.

    - Holds a single AsyncOpenAI client
    - Generates payloads for text and image messages
    - Executes requests asynchronously
    - Returns response text and token usage in a single call
    """

    def __init__(self, model: str, base_url: str, api_key: str, default_headers: Optional[Dict[str, str]] = None, ) -> None:
        self.model: str = model
        self.default_payload_config: Dict[str, Any] = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 8000,
        }

        # Async OpenAI client (non-blocking)
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers=default_headers or {},
        )

        logger.info(f"LLMService initialized with model: {model}")

    def set_model(self, model: str) -> None:
        """
        Sets the model

        Args:
            model (str): The model to use
        """
        logger.info(f"Switching model from {self.model} to {model}")
        self.model = model

    def update_payload_config(self, config: Dict[str, Any]) -> None:
        """
        Update generation parameters.

        Args:
            config: Dictionary with any of: temperature, top_p, max_tokens
        """
        for k in ("temperature", "top_p", "max_tokens"):
            if k in config:
                self.default_payload_config[k] = config[k]
                logger.debug(f"Updated {k} to {config[k]}")

    def get_llm_payload(self, system_prompt: str, user_prompt: str, message_type: str = "text", media_base64: Optional[str] = None, ) -> Dict[str, Any]:
        """
        Build chat completion payload for OpenAI-compatible API.

        Args:
            system_prompt: System instruction/context
            user_prompt: User's message/question
            message_type: "text" or "image" (for multimodal)
            media_base64: Base64-encoded image data (required if message_type="image")

        Returns:
            Complete payload dictionary ready for API call
        """

        if message_type == "image" and media_base64:
            logger.debug("Building multimodal (image) payload")
            return {
                "messages": [{
                    "role": "system",
                    "content": system_prompt
                }, {
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": user_prompt
                    }, {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{media_base64}"
                        },
                    }, ],
                }, ],
                "model": self.model, **self.default_payload_config,
            }
        else:
            logger.debug("Building text-only payload")
            return {
                "messages": [{
                    "role": "system",
                    "content": system_prompt
                }, {
                    "role": "user",
                    "content": user_prompt
                }, ],
                "model": self.model, **self.default_payload_config,
            }

    async def make_llm_request(self, payload: Dict[str, Any]) -> Tuple[str, int]:
        """
        Execute the chat completion asynchronously.

        Args:
            payload: Complete request payload from get_llm_payload()

        Returns:
            Tuple of (response_text, token_count)
        """

        try:
            logger.debug(f"Making LLM request to model: {payload.get('model')}")
            completion = await self.client.chat.completions.create(**payload)

            response_text = completion.choices[0].message.content or ""
            token_count = completion.usage.total_tokens if completion.usage else 0

            logger.info(f"LLM response received. Tokens used: {token_count}")
            return response_text, token_count

        except Exception as e:
            logger.error(f"Error making LLM request: {e}", exc_info=True)
            raise

    async def make_llm_request_with_tracking(self, system_prompt: str, user_prompt: str, message_type: str = "text", media_base64:Optional[str] = None, ) -> Tuple[str, int]:
        """
        Execute the chat completion asynchronously while tracking tokens.

        Args:
            system_prompt: System instruction/context
            user_prompt: User's message/question
            message_type: "text" or "image" (for multimodal)
            media_base64: Base64-encoded image data (required if message_type="image")

        Returns:
            Tuple of (response_text, token_count)
        """

        payload = self.get_llm_payload(system_prompt, user_prompt, message_type, media_base64)

        response_text, token_count = await self.make_llm_request(payload)
        return response_text, token_count
