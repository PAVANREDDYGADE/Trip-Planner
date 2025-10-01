from config import Config
import google.generativeai as genai
from openai import OpenAI
import os

class AIClient:
    def __init__(self):
        self.provider = Config.PROVIDER

        if self.provider == "gemini":
            # Use GOOGLE_APPLICATION_CREDENTIALS env var service account JSON auth
            # No need to check GEMINI_API_KEY environment variable here
            genai.configure()  # It will pick up credentials automatically
            self.model = genai.GenerativeModel("models/gemini-2.5-flash")

        elif self.provider == "openai":
            if not Config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not set.")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL

        else:
            raise ValueError("Unsupported provider.")

    def generate_itinerary(self, prompt):
        if self.provider == "gemini":
            resp = self.model.generate_content(prompt)
            text = getattr(resp, "text", "") or ""
            return text
        elif self.provider == "openai":
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return completion.choices[0].message.content
