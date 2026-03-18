import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcss from '@tailwindcss/vite';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  plugins: [vue(), tailwindcss()],
  server: {
    proxy: {
      // only used during `npm run dev`
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
});
