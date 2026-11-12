
import type { StudyRequest, StudyResponse } from '../types/study'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export class StudyApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message)
    this.name = 'StudyApiError'
  }
}

export async function generateStudyContent(
  request: StudyRequest,
): Promise<StudyResponse> {
  let response: Response

  try {
    response = await fetch(`${API_URL}/study`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })
  } catch {
    throw new Error(
      'Não foi possível conectar ao EducaIA. Verifique se o backend está funcionando.',
    )
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)

    const detail = errorData?.detail

    const message =
      typeof detail === 'string'
        ? detail
        : response.status === 422
          ? 'Os dados enviados são inválidos. Verifique o texto informado.'
          : 'Não foi possível processar seu conteúdo. Tente novamente.'

    throw new StudyApiError(message, response.status)
  }

  return (await response.json()) as StudyResponse
}
