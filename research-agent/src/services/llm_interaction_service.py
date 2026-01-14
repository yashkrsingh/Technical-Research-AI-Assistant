import asyncio
import json
import re
from typing import Dict, Optional, List, Any

import json_repair
from loguru import logger
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionContentPartImageParam, ChatCompletionContentPartTextParam

from domain.interfaces.llm_interaction_interface import LlmInteractionInterface
from infrastructure.llm.llm_service import LLMService


class LlmInteractionService(LlmInteractionInterface):
    """
    High-level orchestration layer for all LLM interactions.

    Responsibilities:
    - Build structured messages (text / image)
    - Handle retries and resilience
    - Normalize LLM output into clean JSON
    """

    SYSTEM_PROMPT = f"""
        \n\nPlease only return a JSON response without any additional text, symbols or explanation. This is important because
        this output would be further processed by interacting systems and apps which require a clean, machine-readable format.
        Extra text or formating interferes with data parsing and can lead to errors or inefficiencies.
        """

    _semaphore = asyncio.Semaphore(10)

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def make_llm_call(self,
                            system_prompt: Optional[str],
                            user_prompt: str, model: Optional[str] = None,
                            message_type: str = "text",
                            media_base64: Optional[str] = None, ) -> Dict:
        """
        Executes an LLM request with retries, validation, and structured output.
        """

        max_parse_attempts = 3
        last_raw_response = None
        last_tokens = 0

        # messages = self._build_gpt5_input(system_prompt=system_prompt,
        #     user_prompt=user_prompt,
        #     message_type=message_type,
        #     media_base64=media_base64, )

        messages = self._build_messages(system_prompt=system_prompt,
                                          user_prompt=user_prompt,
                                          message_type=message_type,
                                          media_base64=media_base64, )
        logger.debug(messages)

        for attempt in range(1, max_parse_attempts + 1):
            response, tokens = await self._safe_llm_call_with_retries(self.llm_service.chat, messages, )

            last_raw_response = response
            last_tokens = tokens

            logger.debug(f"LLM response: {response}")

            parsed = self._parse_llm_response(response)

            if parsed is not None:
                return {
                    "response": parsed,
                    "tokens": tokens,
                }

            logger.warning(f"LLM parse failed (attempt {attempt}/{max_parse_attempts}). Retrying...")

        # All parse attempts failed
        logger.error("LLM returned invalid output after %d attempts. Last raw response: %s, tokens: %s",
            max_parse_attempts,
            last_raw_response, last_tokens)

        raise RuntimeError("LLM returned invalid or non-JSON output after multiple attempts")

    async def get_embedding(self, text: str):
        return await self.llm_service.embed(text)

    # ------------------------------------------------------------------
    # Internal Methods
    # ------------------------------------------------------------------

    def _build_messages(self, system_prompt: Optional[str], user_prompt: str, message_type: str, media_base64: Optional[str], ) -> List[ChatCompletionMessageParam]:
        """
        Builds messages for GPT4 or less conversational models
        """

        messages: List[ChatCompletionMessageParam] = []

        if system_prompt:
            system_message: ChatCompletionSystemMessageParam = {
                "role": "system",
                "content": system_prompt.strip() + "\n" + self.SYSTEM_PROMPT,
            }
            messages.append(system_message)

        if message_type == "image":
            if not media_base64:
                raise ValueError("media_base64 required for image messages")

            text_part: ChatCompletionContentPartTextParam = {
                "type": "text",
                "text": user_prompt,
            }

            image_part: ChatCompletionContentPartImageParam = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{media_base64}"
                },
            }

            user_message: ChatCompletionUserMessageParam = {
                "role": "user",
                "content": [text_part, image_part],
            }

        else:
            user_message: ChatCompletionUserMessageParam = {
                "role": "user",
                "content": user_prompt,
            }

        messages.append(user_message)
        return messages


    def _build_gpt5_input(self, system_prompt: Optional[str], user_prompt: str, message_type: str, media_base64: Optional[str], ) -> List[Dict[str, Any]]:
        """
        Builds GPT-5 compatible multimodal input blocks for the Responses API.
        """

        input_blocks: List[Dict[str, Any]] = []

        # -------------------------
        # System prompt
        # -------------------------
        if system_prompt:
            input_blocks.append({
                "role": "system",
                "content": [{
                    "type": "input_text",
                    "text": system_prompt.strip() + "\n" + self.SYSTEM_PROMPT,
                }],
            })

        # -------------------------
        # User message
        # -------------------------
        user_content: List[Dict[str, Any]] = [{
            "type": "input_text",
            "text": user_prompt,
        }]

        if message_type == "image":
            if not media_base64:
                raise ValueError("media_base64 required for image messages")

            user_content.append({
                "type": "input_image",
                "image_base64": media_base64,
            })

        input_blocks.append({
            "role": "user",
            "content": user_content,
        })

        return input_blocks


    async def _safe_llm_call_with_retries(self, func, *args, max_retries: int = 3, base_delay: float = 1.0, **kwargs, ):
        last_exception = None

        for attempt in range(1, max_retries + 1):
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                last_exception = e
                err = str(e).lower()

                if "timeout" in err or "503" in err or "service unavailable" in err:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))
                        logger.warning(f"[LLM Retry] Attempt {attempt}/{max_retries}, retrying in {delay:.1f}s")
                        await asyncio.sleep(delay)
                        continue

                logger.error(str(e))
                logger.error("LLM call failed", exc_info=True)
                break

        raise RuntimeError(f"LLM failed after {max_retries} retries") from last_exception


    def _parse_llm_response(self, llm_response: str) -> Optional[Dict]:
        """
        Extract valid JSON from the LLM response.
        """
        if not llm_response:
            return None

        llm_response = llm_response.strip()

        try:
            json_parsed = json_repair.loads(llm_response)

            if isinstance(json_parsed, dict):
                if "response" in json_parsed:
                    return json_parsed["response"]
                return json_parsed

        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON response from LLM, trying Regex")
            logger.warning(f"JSON Decode Error: {str(e)}")

        patterns = [r"\{.*\}", r"\[.*\]"]

        for pattern in patterns:
            match = re.search(pattern, llm_response, re.DOTALL)
            if match:
                json_str = match.group()
                try:
                    parsed = json.loads(json_str)
                    if isinstance(parsed, dict) and "response" in parsed:
                        return parsed["response"]
                    return parsed
                except json.JSONDecodeError as e:
                    logger.info(f"Could not parse JSON response with regex: {llm_response}")

        return None
