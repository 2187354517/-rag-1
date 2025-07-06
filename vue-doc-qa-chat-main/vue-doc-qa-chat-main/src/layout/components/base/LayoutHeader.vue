<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '../../../stores/auth'
const userStore = useAuthStore()

const appStore = useAppStore()
const router = useRouter()


const viteTitle = computed(() => {
  return appStore.title
})

const userName = computed(() => {
  return userStore.userInfo?.id || '未登录'
})

const avatar = computed(() => {
  const userId = userStore.userInfo?.id
  return userId ? `/src/assets/${userId}.jpg` : '/src/assets/logo.svg'
})

const handleLogout = () => {
  // 退出登录逻辑
  router.push('/')
}

</script>

<template>
  <div class="header">
    <div>
      <img src="@/assets/logo.jpg" alt="" />
      <span>{{ viteTitle }}</span>
    </div>
    <div class="header-actions">
      <img :size="30" :src="avatar" />
      <span class="user-name">{{ userName }}</span>

      <el-button type="text" @click="handleLogout">退出</el-button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--el-header-height);
  padding-left: 0;
  font-size: 20px;
  color: #fff;

  >div {
    display: flex;
    align-items: center;
    gap: 10px;

    img {
      height: 30px;
    }

    span {
      margin-left: 5px;
    }

    .user-name {
      font-size: 14px;
    }
  }

  .header-actions {
    gap: 10px;
  }
}
</style>
