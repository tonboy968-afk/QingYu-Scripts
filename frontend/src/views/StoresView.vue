<template>
  <div style="padding: 20px;">
    <h1>店铺管理与售后规则</h1>
    
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>店铺列表</span>
              <el-button type="success" size="small" @click="openStoreCreateDialog">新建店铺</el-button>
            </div>
          </template>
          <el-table :data="storesList" style="width: 100%" @row-click="selectStore">
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="platform" label="平台" width="120" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click.stop="openStoreEditDialog(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click.stop="handleDeleteStore(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <el-card v-if="selectedStore">
          <template #header>
            <div class="card-header">
              <span>{{ selectedStore.name }} - 售后规则</span>
              <el-button type="success" size="small" @click="openRuleCreateDialog">新增规则</el-button>
            </div>
          </template>
          <el-table :data="rulesList" style="width: 100%">
            <el-table-column prop="rule_type" label="类型" width="100" />
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="content" label="内容" show-overflow-tooltip />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="openRuleEditDialog(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDeleteRule(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        <el-card v-else>
          <div style="padding: 20px; text-align: center; color: #999;">
            请选择左侧店铺以查看和编辑售后规则
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 店铺弹窗 -->
    <el-dialog v-model="storeDialogVisible" :title="storeDialogTitle">
      <el-form :model="storeForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="storeForm.name" />
        </el-form-item>
        <el-form-item label="平台">
          <el-input v-model="storeForm.platform" placeholder="如：淘宝/京东/拼多多/抖音" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="storeForm.notes" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="storeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveStore">保存</el-button>
      </template>
    </el-dialog>

    <!-- 规则弹窗 -->
    <el-dialog v-model="ruleDialogVisible" :title="ruleDialogTitle">
      <el-form :model="ruleForm" label-width="80px">
        <el-form-item label="类型">
          <el-select v-model="ruleForm.rule_type" placeholder="请选择类型">
            <el-option label="退款" value="退款" />
            <el-option label="运费" value="运费" />
            <el-option label="时效" value="时效" />
            <el-option label="纠纷" value="纠纷" />
            <el-option label="备注" value="备注" />
          </el-select>
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="ruleForm.title" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="ruleForm.content" type="textarea" :rows="5" />
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
import { getStores, createStore, updateStore, deleteStore } from '../api/stores.js'
import { getRules, createRule, updateRule, deleteRule } from '../api/rules.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const storesList = ref([])
const selectedStore = ref(null)
const rulesList = ref([])

const storeDialogVisible = ref(false)
const storeDialogTitle = ref('新建店铺')
const storeForm = ref({ name: '', platform: '', notes: '' })
let editingStoreId = null

const ruleDialogVisible = ref(false)
const ruleDialogTitle = ref('新增规则')
const ruleForm = ref({ store_id: null, rule_type: '', title: '', content: '' })
let editingRuleId = null

const loadStores = async () => {
  try {
    const res = await getStores()
    storesList.value = res.data || []
  } catch (e) {
    ElMessage.error('加载店铺失败')
  }
}

const selectStore = (store) => {
  selectedStore.value = store
  loadRules(store.id)
}

const loadRules = async (storeId) => {
  try {
    const res = await getRules({ store_id: storeId })
    rulesList.value = res.data || []
  } catch (e) {
    ElMessage.error('加载规则失败')
  }
}

const openStoreCreateDialog = () => {
  storeDialogTitle.value = '新建店铺'
  storeForm.value = { name: '', platform: '', notes: '' }
  editingStoreId = null
  storeDialogVisible.value = true
}

const openStoreEditDialog = (row) => {
  storeDialogTitle.value = '编辑店铺'
  storeForm.value = { ...row }
  editingStoreId = row.id
  storeDialogVisible.value = true
}

const saveStore = async () => {
  try {
    if (editingStoreId) {
      await updateStore(editingStoreId, storeForm.value)
      ElMessage.success('更新成功')
    } else {
      await createStore(storeForm.value)
      ElMessage.success('创建成功')
    }
    storeDialogVisible.value = false
    loadStores()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const handleDeleteStore = (id) => {
  ElMessageBox.confirm('确定删除此店铺吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await deleteStore(id)
      ElMessage.success('删除成功')
      loadStores()
      if (selectedStore.value && selectedStore.value.id === id) {
        selectedStore.value = null
        rulesList.value = []
      }
    } catch (e) {
      ElMessage.error('删除失败')
    }
  })
}

const openRuleCreateDialog = () => {
  if (!selectedStore.value) return ElMessage.warning('请先选择店铺')
  ruleDialogTitle.value = '新增规则'
  ruleForm.value = { store_id: selectedStore.value.id, rule_type: '', title: '', content: '' }
  editingRuleId = null
  ruleDialogVisible.value = true
}

const openRuleEditDialog = (row) => {
  ruleDialogTitle.value = '编辑规则'
  ruleForm.value = { ...row }
  editingRuleId = row.id
  ruleDialogVisible.value = true
}

const saveRule = async () => {
  try {
    if (editingRuleId) {
      await updateRule(editingRuleId, ruleForm.value)
      ElMessage.success('更新成功')
    } else {
      await createRule(ruleForm.value)
      ElMessage.success('创建成功')
    }
    ruleDialogVisible.value = false
    if (selectedStore.value) loadRules(selectedStore.value.id)
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const handleDeleteRule = (id) => {
  ElMessageBox.confirm('确定删除此规则吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await deleteRule(id)
      ElMessage.success('删除成功')
      if (selectedStore.value) loadRules(selectedStore.value.id)
    } catch (e) {
      ElMessage.error('删除失败')
    }
  })
}

onMounted(() => {
  loadStores()
})
</script>
