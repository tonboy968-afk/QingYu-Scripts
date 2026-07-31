<template>
  <div class="store-rules-container">
    <div class="top-bar glass-card">
      <div class="left-section">
        <button class="back-btn" @click="goBack">
          <i class="el-icon-arrow-left"></i> 返回看板
        </button>
        <h2 class="page-title">{{ storeName }} - 售后规则设置</h2>
      </div>
      <button class="add-rule-btn primary" @click="openAddRuleDialog">
        <i class="el-icon-plus"></i> 新增售后规则
      </button>
    </div>

    <div class="rules-section glass-card">
      <div v-if="loading" class="loading-state">加载中...</div>
      <div v-else-if="rules.length === 0" class="empty-state">
        <i class="el-icon-document"></i>
        <p>暂无售后规则，请点击右上角新增</p>
      </div>
      <div v-else class="rules-list">
        <div 
          v-for="rule in rules" 
          :key="rule.id" 
          class="rule-card glass-card"
        >
          <div class="rule-header">
            <div class="rule-type-tag" :class="rule.rule_type">
              {{ rule.rule_type }}
            </div>
            <h3 class="rule-title">{{ rule.title }}</h3>
          </div>
          <div class="rule-content">
            {{ rule.content }}
          </div>
          <div class="rule-footer">
            <span class="update-time">更新时间: {{ formatTime(rule.updated_at) }}</span>
            <div class="action-icons">
              <button class="icon-btn" @click="editRule(rule)" title="编辑">
                <i class="el-icon-edit"></i>
              </button>
              <button class="icon-btn danger" @click="handleDeleteRule(rule.id)" title="删除">
                <i class="el-icon-delete"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Rule Dialog -->
    <el-dialog v-model="ruleDialogVisible" :title="isEditing ? '编辑售后规则' : '新增售后规则'" width="600px" class="premium-dialog">
      <el-form :model="ruleForm" label-width="80px">
        <el-form-item label="规则类型">
          <el-select v-model="ruleForm.rule_type" placeholder="请选择规则类型" style="width: 100%;">
            <el-option label="退款" value="退款" />
            <el-option label="运费" value="运费" />
            <el-option label="时效" value="时效" />
            <el-option label="纠纷" value="纠纷" />
            <el-option label="备注" value="备注" />
          </el-select>
        </el-form-item>
        <el-form-item label="规则标题">
          <el-input v-model="ruleForm.title" placeholder="请输入规则标题" />
        </el-form-item>
        <el-form-item label="规则内容">
          <el-input v-model="ruleForm.content" type="textarea" :rows="6" placeholder="请输入售后规则内容..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ruleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRule">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStores } from '../api/stores.js'
import { getRules, createRule, updateRule, deleteRule as apiDeleteRule } from '../api/rules.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const storeId = route.query.store_id

const storeName = ref('未知店铺')
const rules = ref([])
const loading = ref(false)

const ruleDialogVisible = ref(false)
const isEditing = ref(false)
const ruleForm = ref({ store_id: storeId, rule_type: '', title: '', content: '' })

onMounted(async () => {
  if (!storeId) {
    ElMessage.error('未指定店铺ID')
    goBack()
    return
  }
  
  try {
    // Load store name
    const storesRes = await getStores()
    const store = (storesRes.data || []).find(s => s.id == storeId)
    if (store) storeName.value = store.name
    
    await loadRules()
  } catch (e) {
    console.error('Failed to load store/rules', e)
  }
})

const loadRules = async () => {
  loading.value = true
  try {
    const res = await getRules({ store_id: storeId })
    rules.value = res.data || []
  } catch (e) {
    ElMessage.error('加载售后规则失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/dashboard')
}

const openAddRuleDialog = () => {
  isEditing.value = false
  ruleForm.value = { store_id: storeId, rule_type: '', title: '', content: '' }
  ruleDialogVisible.value = true
}

const editRule = (rule) => {
  isEditing.value = true
  ruleForm.value = { ...rule }
  ruleDialogVisible.value = true
}

const saveRule = async () => {
  try {
    if (isEditing.value && ruleForm.value.id) {
      await updateRule(ruleForm.value.id, ruleForm.value)
      ElMessage.success('更新成功')
    } else {
      await createRule(ruleForm.value)
      ElMessage.success('创建成功')
    }
    ruleDialogVisible.value = false
    loadRules()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const handleDeleteRule = (id) => {
  ElMessageBox.confirm('确定删除此售后规则吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await apiDeleteRule(id)
      ElMessage.success('删除成功')
      loadRules()
    } catch (e) {
      ElMessage.error('删除失败')
    }
  })
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.store-rules-container {
  padding: 24px;
  max-width: 1000px;
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
  font-size: 20px;
  font-weight: 600;
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.add-rule-btn.primary {
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

.add-rule-btn.primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.rules-section {
  padding: 24px;
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

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.rule-card {
  padding: 20px;
  transition: all 0.3s ease;
}

.rule-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.4);
  border-color: rgba(56, 189, 248, 0.3);
}

.rule-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.rule-type-tag {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 500;
}

.rule-type-tag.退款 { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.rule-type-tag.运费 { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.rule-type-tag.时效 { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
.rule-type-tag.纠纷 { background: rgba(139, 92, 246, 0.2); color: #8b5cf6; }
.rule-type-tag.备注 { background: rgba(148, 163, 184, 0.2); color: #94a3b8; }

.rule-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #f8fafc;
}

.rule-content {
  font-size: 14px;
  color: #cbd5e1;
  line-height: 1.6;
  margin-bottom: 16px;
}

.rule-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.update-time {
  font-size: 12px;
  color: #64748b;
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

.icon-btn.danger {
  color: #ef4444;
}

.icon-btn.danger:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
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
