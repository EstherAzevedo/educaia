
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Literal

import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google.genai import errors

from ai_service import generate_study_content


# Configuração dos logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="EducaIA API",
    description="API do assistente de estudos com IA generativa",
    version="0.4.0"
)

# Configuração de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# Modelo dos dados recebidos
class StudyRequest(BaseModel):
    text: str = Field(
        min_length=20,
        max_length=12000,
        description="Texto que o usuário deseja estudar"
    )

    task: Literal["summarize", "explain", "quiz"]


# Modelo dos dados devolvidos
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

    try:
        # Solicita o processamento do conteúdo pela IA
        result = generate_study_content(
            text=request.text,
            task=request.task
        )

    except errors.APIError as exc:
        # Erros retornados pela API do Gemini
        logger.error(
            "Erro na API Gemini. Código: %s. Mensagem: %s",
            exc.code,
            exc.message
        )

        if exc.code in (429, 503):
            raise HTTPException(
                status_code=503,
                detail=(
                    "O serviço de IA está temporariamente indisponível "
                    "ou atingiu um limite de utilização. Tente novamente."
                )
            ) from exc

        raise HTTPException(
            status_code=502,
            detail="Não foi possível obter uma resposta do serviço de IA."
        ) from exc

    except httpx.TimeoutException as exc:
        # O serviço demorou além do tempo limite
        logger.warning("Tempo limite excedido na comunicação com o Gemini.")

        raise HTTPException(
            status_code=504,
            detail="O serviço de IA demorou para responder. Tente novamente."
        ) from exc

    except httpx.RequestError as exc:
        # Problemas de conexão ou comunicação
        logger.exception("Falha de comunicação com o Gemini.")

        raise HTTPException(
            status_code=502,
            detail="Não foi possível estabelecer comunicação com o serviço de IA."
        ) from exc

    except Exception as exc:
        # Outros erros inesperados
        logger.exception("Erro inesperado ao processar solicitação.")

        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro interno ao processar sua solicitação."
        ) from exc

    return {
        "status": "success",
        "task": request.task,
        "message": "Conteúdo processado com sucesso!",
        "result": result,
        "characters": len(request.text)
    }
