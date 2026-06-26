from typing import Any, Dict, Protocol


class AIPort(Protocol):
    async def generate_completion(self, prompt: str, system_instruction: str = "") -> str:
        """Envía un prompt a un modelo LLM y retorna el texto generado."""
        ...

    async def analyze_document(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        """Analiza un documento (póliza, cotización, etc.) usando capacidades multimodales."""
        ...
