# -rag-1
基础的rag项目，基于本地部署的。


  src
  ├─api                 # api接口
  │  ├─chat             # 聊天接口
  │  ├─chatSession      # 聊天历史管理接口
  │  └─documents        # 文档管理接口，包含向量化api
  ├─assets              # 静态资源文件
  ├─components          # 公共组件
  │  ├─Dialog           # 表单弹窗
  │  │  └─BaseDialog
  │  ├─Icon             # 图标扩展
  │  └─Loading          # 加载样式
  │      └─ChatLoading
  ├─enums               # 常用枚举
  ├─http                # http 封装
  │  ├─axios            # axios 封装，拦截器处理
  │  ├─fetch            # fetch 封装，拦截器处理
  │  ├─helper           # 内有取消请求封装，状态检查，错误处理
  │  └─types            # http ts 声明
  ├─layout              # 框架布局模块
  │  └─components
  │      └─base
  ├─router              # 路由管理
  ├─stores              # pinia store
  ├─styles              # 全局样式
  │  ├─element          # elementplus 样式
  │  └─markdown         # markdown 样式
  ├─utils               # 公共 utils
  │  └─markdownit       # markdown-it 封装，内有高亮代码，代码块样式美化
  └─views               # 项目所有页面
      ├─chat            # 对话聊天
      │  └─components   # 对话聊天子组件
      ├─documents       # 文档管理
      └─test            # markdown 样式预览
