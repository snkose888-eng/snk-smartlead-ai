import requests
from flask import current_app

class AIServiceError(Exception):
    pass

class AIService:
    def yanit_uret(self, mesaj, gecmis=None):
        api_key = current_app.config.get("GROQ_API_KEY", "")
        context = current_app.config.get("BUSINESS_CONTEXT", "")
        if not api_key:
            return (
                "Demo modu: SNK Dijital Medya reklam ve tanıtım hizmetleri "
                "hakkında yardımcı olabilirim. Canlı yapay zekâ yanıtı için "
                "GROQ_API_KEY tanımlanmalıdır."
            )

        messages = [{"role": "system", "content": context}]
        for item in (gecmis or [])[-10:]:
            if isinstance(item, dict) and item.get("role") in ("user", "assistant"):
                messages.append({"role": item["role"], "content": str(item.get("content", ""))})
        messages.append({"role": "user", "content": mesaj})

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-oss-120b", "messages": messages},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError, IndexError, TypeError) as exc:
            raise AIServiceError("Yapay zekâ servisine şu anda ulaşılamıyor.") from exc

ai_service = AIService()
