
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

from ai_service import generate_study_content


app = FastAPI(
    title="EducaIA API",
    description="API do assistente de estudos com IA generativa",
    version="0.3.0"
)


# Dados recebidos pela API
class StudyRequest(BaseModel):
    text: str = Field(
        min_length=20,
        max_length=12000,
        description="Texto que o usuário deseja estudar"
    )

    task: Literal["summarize", "explain", "quiz"]


# Dados devolvidos pela API
class StudyResponse(BaseModel):
    status: str
    task: str
    message: str
    result: str
    characters: int


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "API do EducaIA está funcionando!"
    }


@app.post("/study", response_model=StudyResponse)
def process_study(request: StudyRequest):

    # Solicita o processamento do conteúdo pela IA
    result = generate_study_content(
        text=request.text,
        task=request.task
    )

    return {
        "status": "success",
        "task": request.task,
        "message": "Conteúdo processado com sucesso!",
        "result": result,
        "characters": len(request.text)
    }
