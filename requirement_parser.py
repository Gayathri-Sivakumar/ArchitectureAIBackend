import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to environment variables or venv/.env."
        )
    return OpenAI(api_key=api_key)

def parse_requirements(text):
    prompt = f"""
Extract functional and non-functional requirements from the following:

{text}

Return strictly in JSON format:
{{
  "functional": [],
  "non_functional": []
}}
"""

    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content