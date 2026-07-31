<template>
  <el-container style="height: 100vh; width: 100vw;">
    <!-- Sidebar -->
    <el-aside width="260px" style="background-color: #1e293b; color: #fff; overflow-y: auto;">
      <div style="height: 64px; line-height: 64px; text-align: center; font-size: 18px; font-weight: bold; background-color: #0f172a; border-bottom: 1px solid #334155;">
        <i class="el-icon-chat-dot-round" style="margin-right: 8px;"></i>客服话术库
      </div>
      <el-menu
        :default-active="activeMenu"
        background-color="#1e293b"
        text-color="#94a3b8"
        active-text-color="#38bdf8"
        router
        style="border-right: none;"
      >
        <el-menu-item index="/dashboard">
          <i class="el-icon-data-line"></i>
          <span>数据概览</span>
        </el-menu-item>
        
        <el-sub-menu index="scripts">
          <template #title>
            <i class="el-icon-document"></i>
            <span>话术库管理</span>
          </template>
          <el-menu-item-group title="话术分类">
            <el-menu-item 
              v-for="cat in categories" 
              :key="cat.id" 
              :index="'/scripts?category=' + cat.id"
            >
              {{ cat.name }}
            </el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>

        <el-sub-menu index="stores">
          <template #title>
            <i class="el-icon-shop"></i>
            <span>店铺与售后规则</span>
          </template>
          <el-menu-item 
            v-for="store in stores" 
            :key="store.id" 
            :index="'/stores?store=' + store.id"
          >
            {{ store.name }}
          </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/categories">
          <i class="el-icon-folder-opened"></i>
          <span>分类设置</span>
        </el-menu-item>
        <el-menu-item index="/stores-full">
          <i class="el-icon-setting"></i>
          <span>店铺与规则设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- Header -->
      <el-header style="background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; height: 64px !important;">
        <div style="font-size: 16px; font-weight: 600; color: #0f172a;">
          {{ pageTitle }}
        </div>
        <div style="display: flex; align-items: center;">
          <el-input
            v-model="globalSearch"
            placeholder="全局搜索话术标题、内容或标签..."
            style="width: 320px; margin-right: 16px;"
            @keyup.enter="handleGlobalSearch"
          >
            <template #prefix>
              <i class="el-icon-search"></i>
            </template>
          </el-input>
          <el-button type="primary" size="default" @click="openCreateScript">
            <i class="el-icon-plus" style="margin-right: 4px;"></i>新建话术
          </el-button>
        </div>
      </el-header>

      <!-- Main Content -->
      <el-main style="background-color: #f1f5f9; padding: 24px; overflow-y: auto;">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCategories } from './api/categories.js'
import { getStores } from './api/stores.js'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => {
  if (route.path === '/dashboard') return '/dashboard'
  if (route.path === '/categories') return '/categories'
  if (route.path === '/stores-full') return '/stores-full'
  if (route.path.startsWith('/scripts')) return '/scripts'
  if (route.path.startsWith('/stores') && !route.path.includes('full')) return '/stores'
  return '/dashboard'
})

const pageTitle = computed(() => {
  if (route.path === '/dashboard') return '数据概览'
  if (route.path === '/categories') return '分类设置'
  if (route.path === '/stores-full') return '店铺与售后规则设置'
  
  const catId = route.query.category
  const storeId = route.query.store
  
  if (catId) {
    const cat = categories.value.find(c => c.id == catId)
    return cat ? `话术库：${cat.name}` : '话术库管理'
  }
  if (storeId) {
    const store = stores.value.find(s => s.id == storeId)
    return store ? `${store.name} - 售后规则` : '店铺与售后规则'
  }
  if (route.path === '/scripts') return '话术库管理：全部话术'
  return '话术库管理'
})

const categories = ref([])
const stores = ref([])
const globalSearch = ref('')

const handleGlobalSearch = () => {
  if (globalSearch.value.trim()) {
    router.push({ path: '/scripts', query: { q: globalSearch.value } })
    globalSearch.value = ''
  }
}

const openCreateScript = () => {
  router.push({ path: '/scripts', query: { action: 'create' } })
}

onMounted(async () => {
  try {
    const [catsRes, storesRes] = await Promise.all([getCategories(), getStores()])
    categories.value = catsRes.data || []
    stores.value = storesRes.data || []
  } catch (e) {
    console.error('Failed to load categories/stores', e)
  }
})
</script>

<style scoped>
.el-aside {
  box-shadow: 2px 0 8px 0 rgba(29, 35, 41, 0.05);
}
.el-header {
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}
.el-menu {
  border-right: none;
}
</style>
