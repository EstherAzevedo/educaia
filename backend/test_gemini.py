
import os
import time
from google.genai import types
from dotenv import load_dotenv
from google import genai


# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Recupera a chave de API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("A variável GEMINI_API_KEY não foi encontrada.")

# 3. Cria o cliente para acessar o Gemini
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=30000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)

# 4. Envia uma solicitação ao modelo

texto_estudo = """
A inteligência artificial generativa tem ampliado as possibilidades
de aplicação da tecnologia na educação. Essas ferramentas podem
auxiliar na personalização do ensino, na produção de materiais
didáticos e no acompanhamento da aprendizagem dos estudantes.

Apesar dos benefícios, sua utilização também apresenta desafios,
como a proteção dos dados pessoais, a possibilidade de respostas
incorretas, os vieses algorítmicos e a necessidade de desenvolver
o pensamento crítico dos estudantes.
"""

prompt = f"""
Você é um assistente de estudos.

Sua tarefa é resumir o texto fornecido pelo estudante.

Instruções:
- Identifique as ideias principais.
- Utilize linguagem clara e objetiva.
- Preserve as informações importantes.
- Não adicione informações que não estejam no texto.
- Organize a resposta em um pequeno resumo.

Texto para resumir:

{texto_estudo}
"""

# Marca o início da chamada
inicio = time.perf_counter()

# Envia a solicitação ao Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="low"
        )
    )
)

# Calcula o tempo de execução
fim = time.perf_counter()

print(f"\nTempo de resposta: {fim - inicio:.2f} segundos")

# 5. Exibe a resposta gerada pela IA
print("\nResposta do Gemini:\n")
print(response.text)
