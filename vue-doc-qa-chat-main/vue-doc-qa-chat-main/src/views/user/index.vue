<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <template #header>
        <h2>{{ isLogin ? '登录' : '注册' }}</h2>
      </template>

      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px" @submit.prevent="handleSubmit">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-form-item v-if="!isLogin" label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>

        <div class="form-footer">
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ isLogin ? '登录' : '注册' }}
          </el-button>

          <el-button type="text" @click="toggleAuthMode">
            {{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { loginApi, registerApi } from '../../api/user/'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive({
  username: 'lyy',
  password: '123456',
  email: ''
})

// 表单验证规则
const formRules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 30, message: '长度在 6 到 30 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
  ]
})

// 状态管理
const isLogin = ref(true)
const loading = ref(false)

// 切换登录/注册模式
const toggleAuthMode = () => {
  isLogin.value = !isLogin.value
  formRef.value?.resetFields()
}

// 处理表单提交
const handleSubmit = async () => {
  try {
    // 验证表单
    await formRef.value?.validate()
    loading.value = true

    if (isLogin.value) {
      // 登录逻辑
      const { data } = await loginApi({
        username: formData.username,
        password: formData.password
      })

      // 存储token和用户信息
      authStore.setAuthData({
        id: formData.username,
        password: formData.password
        // 其他需要的用户字段
      })
      console.log(authStore.userInfo.id)

      ElMessage.success('登录成功')
      router.push('/LayoutClassic')
    } else {
      // 注册逻辑
      const { data } = await registerApi({
        username: formData.username,
        password: formData.password,
        email: formData.email
      })

      ElMessage.success('注册成功')
      toggleAuthMode() // 注册成功后切换到登录界面
    }
  } catch (error: any) {
    console.error('Auth error:', error)
    const errorMessage = error.response?.data?.message || error.message || '操作失败'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.auth-card {
  width: 400px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>