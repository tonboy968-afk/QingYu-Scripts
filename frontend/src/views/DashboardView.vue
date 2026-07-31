<template>
  <div class="dashboard-container">
    <div class="header-section">
      <h1 class="title">客服话术管理中心</h1>
      <p class="subtitle">选择店铺进入话术库，或管理系统售后规则</p>
    </div>

    <div class="stores-grid">
      <!-- Stores -->
      <div 
        v-for="store in stores" 
        :key="store.id" 
        class="store-card glass-card"
      >
        <div class="store-header">
          <div class="store-icon">{{ store.name.charAt(0) }}</div>
          <div class="store-info">
            <h3>{{ store.name }}</h3>
            <span class="platform-tag">{{ store.platform || '未知平台' }}</span>
          </div>
        </div>
        
        <div class="store-actions">
          <button class="action-btn primary" @click="enterScriptManager(store.id)">
            <i class="el-icon-document"></i> 进入话术库
          </button>
          <button class="action-btn secondary" @click="openRulesSettings(store.id)">
            <i class="el-icon-setting"></i> 售后规则设置
          </button>
        </div>
      </div>

      <!-- Add Store Card -->
      <div class="add-store-card glass-card" @click="openAddStoreDialog">
        <div class="add-icon">+</div>
        <span>添加新店铺</span>
      </div>
    </div>

    <!-- Add Store Dialog -->
    <el-dialog v-model="addStoreVisible" title="添加新店铺" width="400px" class="premium-dialog">
      <el-form :model="newStore" label-width="80px">
        <el-form-item label="店铺名称">
          <el-input v-model="newStore.name" placeholder="请输入店铺名称" />
        </el-form-item>
        <el-form-item label="所属平台">
          <el-select v-model="newStore.platform" placeholder="请选择平台" style="width: 100%;">
            <el-option label="淘宝" value="淘宝" />
            <el-option label="京东" value="京东" />
            <el-option label="拼多多" value="拼多多" />
            <el-option label="抖音" value="抖音" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addStoreVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNewStore">确认添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getStores, createStore } from '../api/stores.js'
import { ElMessage } from 'element-plus'

const router = useRouter()
const stores = ref([])
const addStoreVisible = ref(false)
const newStore = ref({ name: '', platform: '' })

onMounted(async () => {
  try {
    const res = await getStores()
    stores.value = res.data || []
  } catch (e) {
    console.error('Failed to load stores', e)
  }
})

const enterScriptManager = (storeId) => {
  // Navigate to script templates with store ID, triggering animation
  router.push({ path: '/scripts/templates', query: { store_id: storeId } })
}

const openRulesSettings = (storeId) => {
  router.push({ path: '/stores/rules', query: { store_id: storeId } })
}

const openAddStoreDialog = () => {
  newStore.value = { name: '', platform: '' }
  addStoreVisible.value = true
}

const saveNewStore = async () => {
  try {
    await createStore(newStore.value)
    ElMessage.success('店铺添加成功')
    addStoreVisible.value = false
    // Reload stores
    const res = await getStores()
    stores.value = res.data || []
  } catch (e) {
    ElMessage.error('添加失败')
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: 48px;
}

.title {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 0 12px 0;
}

.subtitle {
  color: #94a3b8;
  font-size: 16px;
  margin: 0;
}

.stores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.store-card, .add-store-card {
  padding: 24px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.store-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.15);
  border-color: rgba(56, 189, 248, 0.3);
}

.store-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.store-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: #0f172a;
  margin-right: 16px;
}

.store-info h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
}

.platform-tag {
  font-size: 12px;
  color: #94a3b8;
  background: rgba(148, 163, 184, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
}

.store-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.action-btn {
  flex: 1;
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  color: #fff;
}

.action-btn.primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.action-btn.secondary {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.action-btn.secondary:hover {
  background: rgba(148, 163, 184, 0.2);
}

.add-store-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 180px;
  border-style: dashed;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.add-store-card:hover {
  border-color: #38bdf8;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.05);
}

.add-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.premium-dialog .el-dialog {
  background: #1e293b !important;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.premium-dialog .el-dialog__title {
  color: #f8fafc !important;
}

.premium-dialog .el-dialog__body {
  color: #e2e8f0 !important;
}
</style>
