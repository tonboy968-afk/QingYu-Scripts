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
          <div class="store-info">
            <h3>{{ store.name }}</h3>
            <span class="platform-tag">{{ store.platform || '未知平台' }}</span>
          </div>
          <button class="manage-store-btn" @click.stop="openStoreManageDialog(store)" title="管理店铺">
            🛠️ 管理
          </button>
        </div>
        
        <div class="store-actions">
          <button class="action-btn primary" @click="enterScriptManager(store.id)">
            📄 进入话术库
          </button>
          <button class="action-btn secondary" @click="openRulesSettings(store.id)">
            ⚙️ 售后规则
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

    <!-- Store Manage Dialog -->
    <el-dialog v-model="storeManageDialogVisible" :title="(selectedStore?.name || '') + ' - 店铺管理'" width="400px" class="premium-dialog">
      <div class="store-manage-actions">
        <button class="manage-action-btn primary" @click="editStoreFromDialog">
          ✏️ 编辑店铺信息
        </button>
        <button class="manage-action-btn secondary" @click="goToRulesFromDialog">
          ⚙️ 售后规则设置
        </button>
        <button class="manage-action-btn danger" @click="deleteStoreFromDialog">
          🗑️ 删除此店铺
        </button>
      </div>
    </el-dialog>

    <!-- Edit Store Dialog -->
    <el-dialog v-model="editStoreVisible" title="编辑店铺信息" width="400px" class="premium-dialog">
      <el-form :model="editingStore" label-width="80px">
        <el-form-item label="店铺名称">
          <el-input v-model="editingStore.name" placeholder="请输入店铺名称" />
        </el-form-item>
        <el-form-item label="所属平台">
          <el-select v-model="editingStore.platform" placeholder="请选择平台" style="width: 100%;">
            <el-option label="淘宝" value="淘宝" />
            <el-option label="京东" value="京东" />
            <el-option label="拼多多" value="拼多多" />
            <el-option label="抖音" value="抖音" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editStoreVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEditedStore">保存修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getStores, createStore, deleteStore, updateStore } from '../api/stores.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const stores = ref([])
const addStoreVisible = ref(false)
const newStore = ref({ name: '', platform: '' })

// Store manage dialog states
const storeManageDialogVisible = ref(false)
const selectedStore = ref(null)
const editStoreVisible = ref(false)
const editingStore = ref({ name: '', platform: '' })

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

const openStoreManageDialog = (store) => {
  selectedStore.value = store
  storeManageDialogVisible.value = true
}

const editStoreFromDialog = () => {
  storeManageDialogVisible.value = false
  editingStore.value = { ...selectedStore.value }
  editStoreVisible.value = true
}

const goToRulesFromDialog = () => {
  storeManageDialogVisible.value = false
  if (selectedStore.value) {
    openRulesSettings(selectedStore.value.id)
  }
}

const deleteStoreFromDialog = () => {
  storeManageDialogVisible.value = false
  handleDeleteStore(selectedStore.value?.id)
}

const saveEditedStore = async () => {
  try {
    await updateStore(editingStore.value.id, editingStore.value)
    ElMessage.success('店铺信息更新成功')
    editStoreVisible.value = false
    // Reload stores
    const res = await getStores()
    stores.value = res.data || []
  } catch (e) {
    ElMessage.error('更新失败')
  }
}

const handleDeleteStore = (storeId) => {
  ElMessageBox.confirm('确定删除此店铺吗？删除后相关话术和售后规则也将被清理。', '提示', { 
    type: 'warning',
    confirmButtonText: '确认删除',
    cancelButtonText: '取消'
  }).then(async () => {
    try {
      await deleteStore(storeId)
      ElMessage.success('店铺删除成功')
      // Reload stores
      const res = await getStores()
      stores.value = res.data || []
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // User cancelled
  })
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
  position: relative;
}

.store-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.15);
  border-color: rgba(56, 189, 248, 0.3);
}

.store-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
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

.manage-store-btn {
  background: transparent;
  border: 1px solid rgba(148, 163, 184, 0.3);
  color: #e2e8f0;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.manage-store-btn:hover {
  background: rgba(56, 189, 248, 0.1);
  border-color: #38bdf8;
  color: #38bdf8;
}

.store-manage-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 0;
}

.manage-action-btn {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.manage-action-btn.primary {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  color: #fff;
}

.manage-action-btn.primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.manage-action-btn.secondary {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.manage-action-btn.secondary:hover {
  background: rgba(148, 163, 184, 0.2);
}

.manage-action-btn.danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.manage-action-btn.danger:hover {
  background: rgba(239, 68, 68, 0.2);
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
