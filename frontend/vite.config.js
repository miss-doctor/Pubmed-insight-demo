import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/**
 * 构建产物直接输出到 Flask 的静态目录 static/dist，
 * 后端无需任何改动即可托管，评审也不需要安装 Node。
 */
export default defineConfig({
  plugins: [vue()],
  // 与 Flask 的 static 挂载点保持一致，产物由 /static/dist/ 提供
  base: '/static/dist/',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: '../static/dist',
    emptyOutDir: true,
    assetsDir: 'assets',
    chunkSizeWarningLimit: 1200
  },
  server: {
    port: 5173,
    proxy: {
      // 开发模式下把检索请求转发给 Flask
      '/search': 'http://127.0.0.1:5000'
    }
  }
})
