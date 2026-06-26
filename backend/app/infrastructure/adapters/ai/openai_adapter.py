from typing import Any, Dict
from app.application.ports.outputs.ai import AIPort


class OpenAIAdapter(AIPort):
    def __init__(self, api_key: str):
        # TODO(security): Validar que el API Key no sea nulo.
        self.api_key = api_key

    async def generate_completion(self, prompt: str, system_instruction: str = "") -> str:
        # Implementación stub de llamada a la API de OpenAI
        # En producción se importaría `openai.OpenAI`
        return f"OpenAI response for: {prompt[:30]}..."

    async def analyze_document(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        return {"provider": "openai", "analysis": "Stub analysis data"}
