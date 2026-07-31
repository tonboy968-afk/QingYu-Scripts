<template>
  <div class="script-manager-container">
    <!-- Top Bar with Back Button, Title, Search -->
    <div class="top-bar glass-card">
      <div class="left-section">
        <button class="back-btn" @click="goBack">
          <i class="el-icon-arrow-left"></i> 返回看板
        </button>
        <h2 class="page-title">话术模板库</h2>
      </div>
      
      <div class="search-section">
        <el-input
          v-model="searchQuery"
          placeholder="搜索话术标题、内容或标签..."
          class="premium-search"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <i class="el-icon-search"></i>
          </template>
        </el-input>
        <button class="add-script-btn primary" @click="openAddScriptDialog">
          <i class="el-icon-plus"></i> 新增话术
        </button>
      </div>
    </div>

    <!-- Universal Templates Tabs -->
    <div class="templates-section glass-card">
      <div class="templates-tabs">
        <div 
          v-for="template in templates" 
          :key="template.id"
          :class="['template-tab', { active: currentTemplateId === template.id }]"
          @click="selectTemplate(template.id)"
        >
          {{ template.name }}
        </div>
      </div>

      <!-- Script List -->
      <div class="script-list-section">
        <div v-if="loading" class="loading-state">加载中...</div>
        <div v-else-if="scripts.length === 0" class="empty-state">
          <i class="el-icon-document"></i>
          <p>暂无话术，请点击右上角新增</p>
        </div>
        <div v-else class="scripts-grid">
          <div 
            v-for="script in scripts" 
            :key="script.id" 
            class="script-card glass-card"
          >
            <div class="script-header">
              <h4 class="script-title">{{ script.title }}</h4>
              <div class="script-tags">
                <span v-for="tag in (script.tags || '').split(',').filter(t => t)" :key="tag" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
            <div class="script-content">
              {{ script.content }}
            </div>
            <div class="script-footer">
              <div class="meta-info">
                <span>{{ script.category_name || '未分类' }}</span>
                <span>{{ formatTime(script.updated_at) }}</span>
              </div>
              <div class="action-icons">
                <button class="icon-btn" @click="copyScript(script.content)" title="复制">
                  <i class="el-icon-document-copy"></i>
                </button>
                <button class="icon-btn primary" @click="editScript(script)" title="编辑">
                  <i class="el-icon-edit"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Script Dialog -->
    <el-dialog v-model="scriptDialogVisible" :title="isEditing ? '编辑话术' : '新增话术'" width="600px" class="premium-dialog">
      <el-form :model="scriptForm" label-width="80px">
        <el-form-item label="话术标题">
          <el-input v-model="scriptForm.title" placeholder="请输入话术标题" />
        </el-form-item>
        <el-form-item label="所属分类">
          <el-select v-model="scriptForm.category_id" placeholder="请选择分类" style="width: 100%;">
            <el-option 
              v-for="cat in categories" 
              :key="cat.id" 
              :label="cat.name" 
              :value="cat.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="话术内容">
          <el-input v-model="scriptForm.content" type="textarea" :rows="6" placeholder="请输入话术内容..." />
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="scriptForm.tags" placeholder="逗号分隔，如：退款,运费" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="scriptDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveScript">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getScripts, createScript, updateScript } from '../api/scripts.js'
import { getCategories } from '../api/categories.js'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

// Universal templates
const templates = [
  { id: 'pre_sales', name: '产品售前话术' },
  { id: 'after_sales_general', name: '售后通用话术' },
  { id: 'after_sales_entangled', name: '售后纠缠话术' },
  { id: 'backend_appeal', name: '后台申诉话术' },
  { id: 'product_technical', name: '产品技术类话术' }
]

const currentTemplateId = ref('pre_sales')
const searchQuery = ref('')
const scripts = ref([])
const categories = ref([])
const loading = ref(false)

const scriptDialogVisible = ref(false)
const isEditing = ref(false)
const scriptForm = ref({ title: '', content: '', category_id: null, tags: '' })

onMounted(async () => {
  await loadCategories()
  await loadScripts()
})

watch([currentTemplateId, searchQuery], () => {
  loadScripts()
})

const loadCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res.data || []
  } catch (e) {
    console.error('Failed to load categories', e)
  }
}

const loadScripts = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value) {
      params.q = searchQuery.value
    }
    
    // Note: Backend scripts API supports q, category_id, store_id. 
    // We fetch with search query and display all matching scripts.
    const res = await getScripts(params)
    scripts.value = res.data?.items || []
  } catch (e) {
    ElMessage.error('加载话术失败')
  } finally {
    loading.value = false
  }
}

const selectTemplate = (templateId) => {
  currentTemplateId.value = templateId
}

const handleSearch = () => {
  loadScripts()
}

const goBack = () => {
  router.push('/dashboard')
}

const openAddScriptDialog = () => {
  isEditing.value = false
  scriptForm.value = { title: '', content: '', category_id: null, tags: '' }
  scriptDialogVisible.value = true
}

const editScript = (script) => {
  isEditing.value = true
  scriptForm.value = { ...script }
  scriptDialogVisible.value = true
}

const saveScript = async () => {
  try {
    if (isEditing.value && scriptForm.value.id) {
      await updateScript(scriptForm.value.id, scriptForm.value)
      ElMessage.success('更新成功')
    } else {
      await createScript(scriptForm.value)
      ElMessage.success('创建成功')
    }
    scriptDialogVisible.value = false
    loadScripts()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const copyScript = async (content) => {
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (e) {
    ElMessage.error('复制失败')
  }
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.script-manager-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  margin-bottom: 24px;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  background: transparent;
  border: 1px solid rgba(148, 163, 184, 0.3);
  color: #e2e8f0;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(148, 163, 184, 0.1);
  border-color: #38bdf8;
  color: #38bdf8;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.search-section {
  display: flex;
  gap: 16px;
  align-items: center;
}

.premium-search {
  width: 320px;
}

.premium-search .el-input__inner {
  background: rgba(15, 23, 42, 0.6) !important;
  border-color: rgba(148, 163, 184, 0.2) !important;
  color: #f8fafc !important;
}

.premium-search .el-input__inner::placeholder {
  color: #64748b !important;
}

.add-script-btn.primary {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.add-script-btn.primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.templates-section {
  padding: 24px;
}

.templates-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding-bottom: 16px;
}

.template-tab {
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #94a3b8;
  transition: all 0.2s ease;
}

.template-tab:hover {
  background: rgba(56, 189, 248, 0.1);
  color: #38bdf8;
}

.template-tab.active {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(129, 140, 248, 0.2) 100%);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.script-list-section {
  min-height: 400px;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.scripts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.script-card {
  padding: 20px;
  transition: all 0.3s ease;
}

.script-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.4);
  border-color: rgba(56, 189, 248, 0.3);
}

.script-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.script-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #f8fafc;
  flex: 1;
}

.script-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  font-size: 12px;
  padding: 2px 8px;
  background: rgba(56, 189, 248, 0.1);
  color: #38bdf8;
  border-radius: 12px;
}

.script-content {
  font-size: 14px;
  color: #cbd5e1;
  line-height: 1.6;
  margin-bottom: 16px;
  max-height: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.script-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.meta-info {
  font-size: 12px;
  color: #64748b;
  display: flex;
  gap: 12px;
}

.action-icons {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
}

.icon-btn.primary {
  color: #38bdf8;
}

.icon-btn.primary:hover {
  background: rgba(56, 189, 248, 0.2);
  color: #38bdf8;
}
</style>
