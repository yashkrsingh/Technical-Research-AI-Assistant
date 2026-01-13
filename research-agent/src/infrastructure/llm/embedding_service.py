from typing import Optional, List
from google import genai

from config.constants import LLMConstants


class EmbeddingService:
    """Generate text embeddings using Google's Gemini API."""

    def __init__(self, api_key: str):
        self.embedding_model = LLMConstants.GEMINI_EMBEDDING_MODEL
        self.client = genai.Client(api_key=api_key)

    def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding vector for a text string.
        Returns None if text is empty.
        """
        if not text or not text.strip():
            return None

        response = self.client.models.embed_content(
            model=self.embedding_model, contents=[text]
        )

        content_embedding = response.embeddings[0]
        embedding_vector = content_embedding.values
        return embedding_vector
