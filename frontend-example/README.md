# SVV-LoginPage Frontend Example

完整的前端示例应用，展示如何使用SVV-LoginPage认证模块。

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 确保后端正在运行

```bash
# 在另一个终端窗口
cd ..
python example_app.py
```

后端应该运行在 http://localhost:8000

### 3. 启动前端

```bash
npm run dev
```

前端将运行在 http://localhost:5173

## 功能

- ✅ 用户注册页面
- ✅ 用户登录页面
- ✅ Dashboard页面（受保护）
- ✅ JWT认证
- ✅ localStorage持久化
- ✅ 自动重定向
- ✅ Toast通知

## 使用流程

1. 访问 http://localhost:5173
2. 自动重定向到登录页面
3. 点击"Register now"注册新用户
4. 注册成功后返回登录页面
5. 使用刚注册的账号登录
6. 进入Dashboard查看用户信息
7. 刷新页面，session保持登录状态
8. 点击Logout登出

## 项目结构

```
frontend-example/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui组件
│   │   ├── Login.tsx        # 登录页面
│   │   └── Register.tsx     # 注册页面
│   ├── pages/
│   │   └── Dashboard.tsx    # Dashboard页面
│   ├── api/
│   │   ├── client.ts        # Axios配置
│   │   └── auth.ts          # API函数
│   ├── store/
│   │   └── auth.ts          # Zustand状态管理
│   ├── hooks/
│   │   └── use-toast.ts     # Toast hook
│   ├── lib/
│   │   └── utils.ts         # 工具函数
│   ├── App.tsx              # 主应用
│   ├── main.tsx             # 入口文件
│   └── index.css            # 全局样式
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## 技术栈

- React 18
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui
- React Router
- Zustand
- TanStack Query
- React Hook Form + Zod
- Axios

## 环境变量

`.env` 文件：

```
VITE_API_URL=http://localhost:8000
```

## 常见问题

### CORS错误
确保后端启用了CORS中间件，允许来自 http://localhost:5173 的请求。

### API连接失败
确保后端正在运行在 http://localhost:8000

### 组件样式问题
确保已安装所有依赖：`npm install`
