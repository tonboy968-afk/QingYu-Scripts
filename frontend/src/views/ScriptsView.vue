<template>
  <div style="padding: 20px;">
    <h1>话术管理</h1>
    
    <!-- 搜索和筛选 -->
    <el-card style="margin-bottom: 20px;">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="关键词">
          <el-input v-model="filterForm.q" placeholder="标题/内容/标签" @keyup.enter="loadScripts" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filterForm.category_id" placeholder="请选择分类" clearable>
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="店铺">
          <el-select v-model="filterForm.store_id" placeholder="请选择店铺" clearable>
            <el-option
              v-for="store in stores"
              :key="store.id"
              :label="store.name"
              :value="store.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadScripts">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
          <el-button type="success" @click="openCreateDialog">新建话术</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 话术表格 -->
    <el-card>
      <el-table :data="scriptsList" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="store_name" label="店铺" width="120" />
        <el-table-column prop="tags" label="标签" width="150" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button size="small" @click="handleCopy(scope.row.content)">复制</el-button>
            <el-button size="small" type="primary" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button size="small" type="info" @click="viewDetail(scope.row)">详情</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadScripts"
          @current-change="loadScripts"
        />
      </div>
    </el-card>

    <!-- 新建/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="scriptForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="scriptForm.title" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="scriptForm.category_id" placeholder="请选择分类">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="店铺">
          <el-select v-model="scriptForm.store_id" placeholder="请选择店铺（可选）" clearable>
            <el-option v-for="store in stores" :key="store.id" :label="store.name" :value="store.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="scriptForm.tags" placeholder="逗号分隔" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="scriptForm.content" type="textarea" :rows="5" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveScript">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getScripts, createScript, updateScript, deleteScript } from '../api/scripts.js'
import { getCategories } from '../api/categories.js'
import { getStores } from '../api/stores.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const filterForm = ref({ q: '', category_id: null, store_id: null })
const scriptsList = ref([])
const categories = ref([])
const stores = ref([])
const pagination = ref({ page: 1, pageSize: 20, total: 0 })

const dialogVisible = ref(false)
const dialogTitle = ref('新建话术')
const scriptForm = ref({ title: '', content: '', category_id: null, store_id: null, tags: '' })
let editingId = null

const loadScripts = async () => {
  try {
    const params = { ...filterForm.value, page: pagination.value.page, page_size: pagination.value.pageSize }
    const res = await getScripts(params)
    scriptsList.value = res.data?.items || []
    pagination.value.total = res.data?.total || 0
  } catch (e) {
    ElMessage.error('加载话术失败')
  }
}

const loadCategoriesAndStores = async () => {
  try {
    const [cats, storesRes] = await Promise.all([getCategories(), getStores()])
    categories.value = cats.data || []
    stores.value = storesRes.data || []
  } catch (e) {
    console.error('Failed to load categories/stores', e)
  }
}

const resetFilter = () => {
  filterForm.value = { q: '', category_id: null, store_id: null }
  pagination.value.page = 1
  loadScripts()
}

const openCreateDialog = () => {
  dialogTitle.value = '新建话术'
  scriptForm.value = { title: '', content: '', category_id: null, store_id: null, tags: '' }
  editingId = null
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  dialogTitle.value = '编辑话术'
  scriptForm.value = { ...row }
  editingId = row.id
  dialogVisible.value = true
}

const saveScript = async () => {
  try {
    if (editingId) {
      await updateScript(editingId, scriptForm.value)
      ElMessage.success('更新成功')
    } else {
      await createScript(scriptForm.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadScripts()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除此话术吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await deleteScript(id)
      ElMessage.success('删除成功')
      loadScripts()
    } catch (e) {
      ElMessage.error('删除失败')
    }
  })
}

const handleCopy = async (content) => {
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (e) {
    ElMessage.error('复制失败')
  }
}

const viewDetail = (row) => {
  ElMessageBox.alert(row.content, '话术详情', { confirmButtonText: '确定' })
}

onMounted(() => {
  loadCategoriesAndStores()
  loadScripts()
})
</script>
