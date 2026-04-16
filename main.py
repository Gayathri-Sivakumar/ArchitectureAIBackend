from fastapi import FastAPI, HTTPException
from openai import APIConnectionError, APIStatusError, OpenAIError, RateLimitError
from pydantic import BaseModel

from requirement_parser import parse_requirements
from architecture_generator import generate_architecture
from diagram_generator import generate_diagram

app = FastAPI()

class RequestInput(BaseModel):
    text: str


@app.post("/design")
def design_system(req: RequestInput):
    try:
        parsed = parse_requirements(req.text)
        architecture = generate_architecture(parsed)
        diagram = generate_diagram(architecture)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except RateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail=(
                "OpenAI quota/rate limit reached. Check billing or try again later."
            ),
        ) from exc
    except APIConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to OpenAI. Check internet connection and retry.",
        ) from exc
    except APIStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI API error (status {exc.status_code}).",
        ) from exc
    except OpenAIError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {exc}") from exc

    return {
        "requirements": parsed,
        "architecture": architecture,
        "diagram": diagram
    }