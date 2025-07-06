// 
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 样式导入
import '@/styles/reset.scss'                // 重置样式
import '@/styles/markdown/mdmdt-light.scss' // markdown 亮色主题
import '@/styles/markdown/plugins.scss'     // markdown 插件样式
import '@/styles/index.scss'                // 全局自定义样式

// Element Plus 图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 创建应用实例
const app = createApp(App)

// 1. 初始化 Pinia (增强配置)
const pinia = createPinia()
app.use(pinia)

// 2. 安装路由
app.use(router)

// 3. 全局注册 Element Plus 图标 (带类型提示)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 4. 全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('全局捕获的Vue错误:', { err, instance, info })
  // 可以在这里添加错误上报逻辑
}

// 5. 全局属性扩展 (可选)
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $filters: {
      formatDate: (date: Date) => string
    }
  }
}

app.config.globalProperties.$filters = {
  formatDate: (date: Date) => {
    return new Date(date).toLocaleDateString()
  }
}

// 6. 生产环境配置 (可选)
if (import.meta.env.PROD) {
  // 禁用 console.log
  console.log = () => { }
  // 可以添加其他生产环境特定配置
}

// 挂载应用
app.mount('#app')

// 7. 开发环境调试工具
if (import.meta.env.DEV) {
  // 将 pinia 实例挂载到 window 方便调试

  console.log('开发模式已启用，Pinia 实例已挂载到 window.__pinia')
}