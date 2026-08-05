from pathlib import Path
from google import genai
from config.settings import GEMINI_API_KEY

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.prompt_dir = Path("prompts")

    def ask(self, prompt: str) -> str:
        prt = self._load_prompt("ask.txt", prompt=prompt)
        return self._generate(prt)

    def sumarize(self, messages: str, context: str = "") -> str:
        prt = self._load_prompt("summary.txt", context=context, messages=messages)
        return self._generate(prt)

    def _load_prompt(self, filename: str, **kwargs) -> str:
        system_prompt = (
            self.prompt_dir / "system.txt"
        ).read_text(encoding="utf-8")

        template = (
            self.prompt_dir / filename
        ).read_text(encoding="utf-8")

        prompt = f"{system_prompt}\n\n{template}"
        return prompt.format(**kwargs)

    def _generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
            )
            # Debug information
            print("=" * 60)
            print("Response object:")
            print(response)
            print("=" * 60)
            
            if not response.text:
                raise RuntimeError("Gemini returned no text. The prompt may be too long or blocked by safety filters.")
            return response.text
            
        except Exception as e:
            raise RuntimeError(f"Gemini API Error: {e}")