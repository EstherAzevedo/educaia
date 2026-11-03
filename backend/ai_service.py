
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Carrega as variáveis de ambiente
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# Recupera a chave de API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY não foi configurada.")


# Configura o cliente Gemini
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=30000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)


MODEL_NAME = "gemini-3.5-flash-lite"


# Instruções específicas para cada atividade
TASK_PROMPTS = {
    "summarize": """
        Resuma o material fornecido pelo estudante.

        Instruções:
        - Identifique as ideias principais.
        - Utilize linguagem clara e objetiva.
        - Preserve as informações importantes.
        - Não adicione informações que não estejam no texto.
        - Organize a resposta em um pequeno resumo.
    """,

    
    "explain": """
        Explique o conteúdo fornecido pelo estudante.

        Instruções:
        - Utilize linguagem simples e didática.
        - Explique os conceitos importantes passo a passo.
        - Utilize analogias e exemplos quando ajudarem na compreensão.
        - Identifique claramente os exemplos ilustrativos.
        - Preserve a precisão técnica dos conceitos.
        - Não apresente simplificações como regras absolutas.
        - Diferencie as informações do material das explicações complementares.
        - Organize a resposta com títulos e listas quando apropriado.
        - Evite apresentações e conclusões desnecessariamente longas.
    """,


    "quiz": """
        Crie cinco perguntas para ajudar o estudante
        a revisar o conteúdo fornecido.

        Instruções:
        - Crie perguntas de múltipla escolha.
        - Apresente quatro alternativas por pergunta.
        - Indique a alternativa correta.
        - Explique brevemente a resposta correta.
        - Utilize somente informações presentes no material.
    """
}


def generate_study_content(text: str, task: str) -> str:
    """
    Gera conteúdo de estudo utilizando o modelo Gemini.
    """

    instruction = TASK_PROMPTS[task]

    prompt = f"""
    Você é o EducaIA, um assistente de estudos.

    {instruction}

    MATERIAL DE ESTUDO:

    {text}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level="minimal"
            )
        )
    )

    if not response.text:
        raise RuntimeError("O modelo não retornou conteúdo.")

    return response.text.strip()
