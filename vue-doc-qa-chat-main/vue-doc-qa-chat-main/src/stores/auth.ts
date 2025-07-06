import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserResponseType } from '../api/user/types'

export const useAuthStore = defineStore('auth', () => {
    // 用户信息状态
    const userInfo = ref<Omit<UserResponseType, 'created_at'> | null>(null)

    // 设置用户数据 (不再需要token)
    const setAuthData = (data: Omit<UserResponseType, 'created_at'>) => {
        if (!data?.id || typeof data.id !== 'string') {
            console.error('[AuthStore] 无效的用户ID:', data?.id)
            throw new Error('用户ID无效')
        }



        userInfo.value = data
        console.debug('[AuthStore] 用户数据设置成功', data)
    }

    // 清除认证数据
    const clearAuthData = () => {
        userInfo.value = null
        console.debug('[AuthStore] 清除用户数据')
    }

    // 计算属性：是否已认证
    const isAuthenticated = computed(() => !!userInfo.value?.id)

    return {
        userInfo,
        setAuthData,
        clearAuthData,
        isAuthenticated
    }
})