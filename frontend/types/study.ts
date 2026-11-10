
export type StudyTask = 'summarize' | 'explain' | 'quiz'

export interface StudyRequest {
  text: string
  task: StudyTask
}

export interface StudyResponse {
  status: string
  task: StudyTask
  message: string
  result: string
  characters: number
}
