import http from '@/http'
import type { UserRequestType, UserResponseType } from './types'
import type { CustomAxiosConfig } from '@/http/types'
import { v4 as uuidv4 } from 'uuid';
/**
 * 用户登录
 * @param data 登录参数
 * @returns 用户信息和token
 */
const loginApi = (data: Pick<UserRequestType, 'username' | 'password'>) => {
  return http.post<UserResponseType>('/auth/login', data, {
    cancel: false
  } as CustomAxiosConfig)
}

/**
 * 用户注册
 * @param data 注册参数
 * @returns 注册成功的用户信息
 */
const registerApi = (data: UserRequestType) => {
  return http.post<UserResponseType>('/auth/register', {
    id: uuidv4(),
    username: data.username,  // 确保发送username
    password: data.password,
    email: data.email
  }, {
    cancel: false
  } as CustomAxiosConfig)
}

/**
 * 获取用户列表
 * @returns 用户列表
 */
const usersApi = () => {
  return http.get<UserResponseType[]>('/auth/users')
}

/**
 * 更新用户信息
 * @param id 用户ID
 * @param data 用户数据
 * @returns 更新后的用户信息
 */
const usersEditApi = (id: string, data: UserRequestType) => {
  return http.put<UserResponseType>(`/auth/users/${id}`, data)
}

/**
 * 删除用户
 * @param id 用户ID
 * @returns 删除结果
 */
const usersDeleteApi = (id: string) => {
  return http.delete<string>(`/auth/users/${id}`)
}

export {
  loginApi,
  registerApi,
  usersApi,
  usersEditApi,
  usersDeleteApi
}
export * from './types'