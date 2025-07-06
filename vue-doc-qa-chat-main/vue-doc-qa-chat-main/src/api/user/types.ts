export interface UserRequestType {
  id: string      // 必填字段
  username: string
  password: string
  email: string
}

export interface UserResponseType {
  id: string
  username: string
  email: string
  created_at: string
}