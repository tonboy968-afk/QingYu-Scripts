<template>
  <div class="script-manager-container">
    <!-- Top Bar with Back Button, Title -->
    <div class="top-bar glass-card">
      <div class="left-section">
        <button class="back-btn" @click="goBack">
          <i class="el-icon-arrow-left"></i> 返回看板
        </button>
        <h2 class="page-title">话术模板库</h2>
      </div>
    </div>

    <!-- Prominent Search Box -->
    <div class="search-container glass-card">
      <div class="search-wrapper">
        <i class="el-icon-search search-icon"></i>
        <input 
          v-model="searchQuery" 
          @keyup.enter="handleSearch"
          placeholder="搜索话术标题、内容或标签...支持产品名称、规格、功能等关键词"
          class="premium-search-input"
        />
        <button class="search-btn" @click="handleSearch">
          搜 索
        </button>
      </div>
    </div>

    <!-- Universal Templates Tabs with Sub-categories -->
    <div class="templates-section glass-card">
      <div class="templates-tabs-header">
        <span class="tabs-title">话术分类</span>
        <button class="edit-mode-toggle-btn" @click="toggleEditMode">
          {{ isEditMode ? '✔ 退出编辑模式' : '✏️ 进入编辑模式' }}
        </button>
      </div>
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

      <!-- Sub-category Tags -->
      <div v-if="currentSubCategories.length > 0" class="sub-categories-section">
        <div class="sub-tabs-header">
          <span class="sub-tabs-title">细分标签</span>
        </div>
        <div class="sub-categories-tags">
          <div 
            v-for="subCat in currentSubCategories" 
            :key="subCat.id"
            :class="['sub-tag', { active: currentSubCategoryId === subCat.id }]"
            @click="selectSubCategory(subCat.id)"
          >
            {{ subCat.name }}
          </div>
        </div>
      </div>

      <!-- Script List -->
      <div class="script-list-section">
        <div v-if="loading" class="loading-state">加载中...</div>
        <div v-else-if="scripts.length === 0 && !showAddBox" class="empty-state">
          <i class="el-icon-document"></i>
          <p>暂无话术，请点击下方「添加话术」按钮创建</p>
        </div>

        <!-- Scripts Grid -->
        <div v-if="scripts.length > 0 || showAddBox" class="scripts-grid">
          <div 
            v-for="script in scripts" 
            :key="script.id" 
            class="script-card glass-card"
          >
            <div class="script-header">
              <h4 class="script-title">{{ script.title }}</h4>
              <div class="script-actions">
                <template v-if="isEditMode">
                  <button class="icon-btn primary" @click="editScript(script)" title="编辑话术">
                    ✏️ 编辑
                  </button>
                  <button class="icon-btn danger" @click="handleDeleteScript(script.id)" title="删除话术">
                    🗑️ 删除
                  </button>
                </template>
                <template v-else>
                  <button class="icon-btn copy-only" @click="copyScript(script.content)" title="复制话术">
                    📋 复制
                  </button>
                </template>
              </div>
            </div>
            <div class="script-tags">
              <span v-for="tag in (script.tags || '').split(',').filter(t => t)" :key="tag" class="tag">
                #{{ tag }}
              </span>
            </div>
            <div class="script-content">
              {{ script.content }}
            </div>
            <div class="script-footer">
              <span class="meta-info">{{ formatTime(script.updated_at) }}</span>
            </div>
          </div>

          <!-- Add Script Box (Always last) -->
          <div class="add-script-box glass-card" @click="openAddScriptDialog">
            <div class="add-icon-large">+</div>
            <span>添加话术</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Script Dialog -->
    <el-dialog v-model="scriptDialogVisible" :title="isEditing ? '编辑话术' : '新增话术'" width="650px" class="premium-dialog">
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
        <el-form-item label="细分标签">
          <el-select 
            v-model="scriptForm.sub_category_ids" 
            multiple 
            placeholder="请选择细分标签（可选）" 
            style="width: 100%;"
          >
            <el-option 
              v-for="subCat in currentSubCategories" 
              :key="subCat.id" 
              :label="subCat.name" 
              :value="subCat.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="话术内容">
          <el-input v-model="scriptForm.content" type="textarea" :rows="6" placeholder="请输入话术内容..." />
        </el-form-item>
        <el-form-item label="话术标签（自定义）">
          <el-input v-model="scriptForm.tags" placeholder="逗号分隔，如：退款,运费,现货" />
          <div class="tag-hint">💡 注：此处添加的标签将显示在话术卡片上，方便后续搜索和分类</div>
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
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getScripts, createScript, updateScript, deleteScript as apiDeleteScript } from '../api/scripts.js'
import { getCategories } from '../api/categories.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

// Universal templates with sub-categories (matching seed data categories)
const templates = [
  { 
    id: 'pre_sales_single', 
    name: '单产品售前话术',
    subCategories: [
      { id: 'ps_product_intro', name: '产品介绍' },
      { id: 'ps_specs', name: '规格介绍' },
      { id: 'ps_features', name: '功能介绍' },
      { id: 'ps_promo', name: '促销活动' }
    ]
  },
  { 
    id: 'after_sales_general', 
    name: '售后通用话术',
    subCategories: [
      { id: 'as_general_reply', name: '常规回复' },
      { id: 'as_empathy', name: '安抚情绪' },
      { id: 'as_solution', name: '解决方案' }
    ]
  },
  { 
    id: 'after_sales_entangled', 
    name: '产品售后纠缠话术',
    subCategories: [
      { id: 'ae_complaint', name: '客户投诉' },
      { id: 'ae_refund_dispute', name: '退款纠纷' },
      { id: 'ae_escalation', name: '升级处理' }
    ]
  },
  { 
    id: 'backend_appeal', 
    name: '后台申诉话术',
    subCategories: [
      { id: 'ba_platform_rule', name: '平台规则' },
      { id: 'ba_evidence', name: '证据提交' },
      { id: 'ba_complaint_reply', name: '投诉回复' }
    ]
  },
  { 
    id: 'product_technical', 
    name: '产品技术类话术',
    subCategories: [
      { id: 'pt_usage', name: '使用指导' },
      { id: 'pt_troubleshoot', name: '故障排查' },
      { id: 'pt_compatibility', name: '兼容性说明' }
    ]
  }
]

const currentTemplateId = ref('pre_sales')
const currentSubCategoryId = ref(null)
const searchQuery = ref('')
const scripts = ref([])
const categories = ref([])
const loading = ref(false)
const showAddBox = ref(true) // Show add box when no scripts
const isEditMode = ref(false) // Edit mode toggle

const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
}

const scriptDialogVisible = ref(false)
const isEditing = ref(false)
const scriptForm = ref({ 
  title: '', 
  content: '', 
  category_id: null, 
  sub_category_ids: [],
  tags: '' 
})

// Computed sub-categories for current template
const currentSubCategories = computed(() => {
  const tmpl = templates.find(t => t.id === currentTemplateId.value)
  return tmpl ? tmpl.subCategories : []
})

onMounted(async () => {
  await loadCategories()
  // Get store_id from route if exists
  if (route.query.store_id) {
    // We could filter by store if needed
  }
  await loadScripts()
})

watch([currentTemplateId, currentSubCategoryId, searchQuery], () => {
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
  currentSubCategoryId.value = null // Reset sub-category when template changes
}

const selectSubCategory = (subCatId) => {
  currentSubCategoryId.value = currentSubCategoryId.value === subCatId ? null : subCatId
}

const handleSearch = () => {
  loadScripts()
}

const goBack = () => {
  router.push('/dashboard')
}

const openAddScriptDialog = () => {
  isEditing.value = false
  scriptForm.value = { 
    title: '', 
    content: '', 
    category_id: null, 
    sub_category_ids: [],
    tags: '' 
  }
  scriptDialogVisible.value = true
}

const editScript = (script) => {
  isEditing.value = true
  scriptForm.value = { 
    ...script, 
    sub_category_ids: [] // Handle sub-category ids if needed
  }
  scriptDialogVisible.value = true
}

const saveScript = async () => {
  try {
    const submitData = { ...scriptForm.value }
    delete submitData.sub_category_ids // Remove sub_category_ids from submission if backend doesn't support it
    
    if (isEditing.value && scriptForm.value.id) {
      await updateScript(scriptForm.value.id, submitData)
      ElMessage.success('更新成功')
    } else {
      await createScript(submitData)
      ElMessage.success('创建成功')
    }
    scriptDialogVisible.value = false
    loadScripts()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const handleDeleteScript = (id) => {
  ElMessageBox.confirm('确定删除此话术吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await apiDeleteScript(id)
      ElMessage.success('删除成功')
      loadScripts()
    } catch (e) {
      ElMessage.error('删除失败')
    }
  })
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

/* Prominent Search Box */
.search-container {
  padding: 32px 24px;
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
}

.search-wrapper {
  display: flex;
  align-items: center;
  background: rgba(15, 23, 42, 0.8);
  border: 2px solid rgba(56, 189, 248, 0.3);
  border-radius: 16px;
  padding: 8px 8px 8px 24px;
  width: 100%;
  max-width: 700px;
  box-shadow: 0 8px 32px rgba(56, 189, 248, 0.1);
  transition: all 0.3s ease;
}

.search-wrapper:focus-within {
  border-color: #38bdf8;
  box-shadow: 0 8px 32px rgba(56, 189, 248, 0.2);
}

.search-icon {
  font-size: 20px;
  color: #64748b;
  margin-right: 16px;
}

.premium-search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 16px;
  color: #f8fafc;
  padding: 12px 0;
}

.premium-search-input::placeholder {
  color: #64748b;
}

.search-btn {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  color: #fff;
  border: none;
  padding: 12px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Templates Section */
.templates-section {
  padding: 24px;
}

.templates-tabs-header, .sub-tabs-header {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tabs-title, .sub-tabs-title {
  font-size: 14px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.edit-mode-toggle-btn {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-mode-toggle-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.templates-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding-bottom: 16px;
  overflow-x: auto;
}

.template-tab {
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #94a3b8;
  transition: all 0.2s ease;
  white-space: nowrap;
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

/* Sub-categories */
.sub-categories-section {
  margin-bottom: 24px;
}

.sub-categories-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.sub-tag {
  padding: 6px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #94a3b8;
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.2);
  transition: all 0.2s ease;
}

.sub-tag:hover {
  background: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.3);
  color: #38bdf8;
}

.sub-tag.active {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(129, 140, 248, 0.2) 100%);
  color: #38bdf8;
  border-color: rgba(56, 189, 248, 0.4);
}

/* Script List */
.script-list-section {
  min-height: 300px;
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
  position: relative;
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
  margin-right: 12px;
}

.script-actions {
  display: flex;
  gap: 6px;
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

.icon-btn.danger {
  color: #ef4444;
}

.icon-btn.danger:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.script-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 12px;
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
}

.tag-hint {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 6px;
  line-height: 1.4;
}

.icon-btn.copy-only {
  background: transparent;
  border: none;
  color: #38bdf8;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn.copy-only:hover {
  background: rgba(56, 189, 248, 0.1);
  color: #38bdf8;
}

/* Add Script Box */
.add-script-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  border-style: dashed;
  border-color: rgba(56, 189, 248, 0.3);
  color: #94a3b8;
  transition: all 0.3s ease;
  cursor: pointer;
}

.add-script-box:hover {
  border-color: #38bdf8;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.05);
  transform: translateY(-2px);
}

.add-icon-large {
  font-size: 40px;
  margin-bottom: 12px;
  line-height: 1;
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
