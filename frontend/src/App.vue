<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade-slide" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // Initialize any global state if needed
})
</script>

<style>
/* Premium Global Styles */
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --bg-card: rgba(30, 41, 59, 0.6);
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --accent: #38bdf8;
  --accent-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  --border-color: rgba(148, 163, 184, 0.1);
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  color: var(--text-primary);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}

/* Animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Glassmorphism Card Utility */
.glass-card {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
}

/* Element Plus overrides for dark/premium theme */
.el-card {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
}

.el-input__inner, .el-textarea__inner {
  background: rgba(15, 23, 42, 0.6) !important;
  border-color: var(--border-color) !important;
  color: var(--text-primary) !important;
}

.el-dialog {
  background: #1e293b !important;
  border: 1px solid rgba(148, 163, 184, 0.2) !important;
}

.el-dialog__title {
  color: #f8fafc !important;
}

.el-dialog__body {
  color: #e2e8f0 !important;
}

.el-message {
  background: rgba(30, 41, 59, 0.9) !important;
  border: 1px solid var(--border-color) !important;
  color: #f8fafc !important;
}
</style>
