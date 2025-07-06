export interface ChatSessionRequestType {
  id?: string
  title?: string
  user_name: string
}

export interface ChatSessionResponseType {
  id: string
  title: string
  data: string
  user_name: string
}
