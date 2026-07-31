<template>
  <div style="background: #fff; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <!-- Filters -->
    <el-form :inline="true" :model="filterForm" class="mb-4">
      <el-form-item label="关键词">
        <el-input v-model="filterForm.q" placeholder="标题/内容/标签" style="width: 200px;" @keyup.enter="loadScripts" />
      </el-form-item>
      <el-form-item label="店铺">
        <el-select v-model="filterForm.store_id" placeholder="全部店铺" clearable style="width: 150px;">
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
      </el-form-item>
    </el-form>

    <!-- Script Table -->
    <el-table :data="scriptsList" style="width: 100%" v-loading="loading">
      <el-table-column prop="title" label="话术标题" min-width="200" />
      <el-table-column prop="category_name" label="分类" width="150" />
      <el-table-column prop="store_name" label="店铺" width="150" />
      <el-table-column prop="tags" label="标签" width="150">
        <template #default="scope">
          <el-tag v-for="tag in (scope.row.tags || '').split(',')" :key="tag" size="small" style="margin-right: 4px;">{{ tag }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="250" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" link @click="handleCopy(scope.row.content)">复制</el-button>
          <el-button size="small" type="primary" link @click="openEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" link @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
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

    <!-- Create/Edit Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="scriptForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="scriptForm.title" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="scriptForm.category_id" placeholder="请选择分类" style="width: 100%;">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="店铺">
          <el-select v-model="scriptForm.store_id" placeholder="请选择店铺（可选）" clearable style="width: 100%;">
            <el-option v-for="store in stores" :key="store.id" :label="store.name" :value="store.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="scriptForm.tags" placeholder="逗号分隔" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="scriptForm.content" type="textarea" :rows="6" />
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
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getScripts, createScript, updateScript, deleteScript } from '../api/scripts.js'
import { getCategories } from '../api/categories.js'
import { getStores } from '../api/stores.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

const filterForm = ref({ q: '', category_id: null, store_id: null })
const scriptsList = ref([])
const categories = ref([])
const stores = ref([])
const pagination = ref({ page: 1, pageSize: 20, total: 0 })
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('新建话术')
const scriptForm = ref({ title: '', content: '', category_id: null, store_id: null, tags: '' })
let editingId = null

const loadScripts = async () => {
  loading.value = true
  try {
    const params = { ...filterForm.value, page: pagination.value.page, page_size: pagination.value.pageSize }
    // Remove null/undefined values
    Object.keys(params).forEach(key => {
      if (params[key] === null || params[key] === '') delete params[key]
    })
    
    const res = await getScripts(params)
    scriptsList.value = res.data?.items || []
    pagination.value.total = res.data?.total || 0
  } catch (e) {
    ElMessage.error('加载话术失败')
  } finally {
    loading.value = false
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
  // Reset route query
  router.push({ path: route.path, query: {} })
  loadScripts()
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

// Watch route query for category or store filter
watch(() => route.query.category, (newVal) => {
  if (newVal) {
    filterForm.value.category_id = Number(newVal)
  } else {
    filterForm.value.category_id = null
  }
  pagination.value.page = 1
  loadScripts()
})

watch(() => route.query.store, (newVal) => {
  if (newVal) {
    filterForm.value.store_id = Number(newVal)
  } else {
    filterForm.value.store_id = null
  }
  pagination.value.page = 1
  loadScripts()
})

watch(() => route.query.q, (newVal) => {
  filterForm.value.q = newVal || ''
  pagination.value.page = 1
  loadScripts()
})

onMounted(async () => {
  await loadCategoriesAndStores()
  
  // Init filters from route query
  if (route.query.category) filterForm.value.category_id = Number(route.query.category)
  if (route.query.store) filterForm.value.store_id = Number(route.query.store)
  if (route.query.q) filterForm.value.q = route.query.q

  loadScripts()
})
</script>

<style scoped>
.mb-4 {
  margin-bottom: 16px;
}
</style>
