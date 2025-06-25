// frontend/vite.config.js
import { defineConfig } from 'vite'
import path from 'path'
import react from '@vitejs/plugin-react'

// Optional: use alias if needed
export default defineConfig({
  root: '.', // Ensure it's pointing at your frontend directory
  base: './',
  build: {
    outDir: 'dist'
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  plugins: [react()],
})
