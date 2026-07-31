<template>
  <div style="padding: 20px;">
    <h1>分类管理</h1>
    
    <el-card style="margin-bottom: 20px;">
      <el-button type="success" @click="openCreateDialog">新建分类</el-button>
    </el-card>

    <el-card>
      <el-table :data="categoriesList" style="width: 100%">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column prop="script_count" label="话术数量" width="100" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="categoryForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="categoryForm.name" />
        </el-form-item>
        <el-form-item label="类型">
          <el-input v-model="categoryForm.type" placeholder="如：售前/售后/申诉/技术" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="categoryForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCategory">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories, createCategory, updateCategory, deleteCategory } from '../api/categories.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const categoriesList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新建分类')
const categoryForm = ref({ name: '', type: '', sort_order: 0 })
let editingId = null

const loadCategories = async () => {
  try {
    const res = await getCategories()
    categoriesList.value = res.data || []
  } catch (e) {
    ElMessage.error('加载分类失败')
  }
}

const openCreateDialog = () => {
  dialogTitle.value = '新建分类'
  categoryForm.value = { name: '', type: '', sort_order: 0 }
  editingId = null
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  dialogTitle.value = '编辑分类'
  categoryForm.value = { ...row }
  editingId = row.id
  dialogVisible.value = true
}

const saveCategory = async () => {
  try {
    if (editingId) {
      await updateCategory(editingId, categoryForm.value)
      ElMessage.success('更新成功')
    } else {
      await createCategory(categoryForm.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadCategories()
  } catch (e) {
    if (e.response && e.response.status === 400) {
      ElMessage.error(e.response.data?.detail || '分类下有话术，无法删除或重名')
    } else {
      ElMessage.error('保存失败')
    }
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除此分类吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await deleteCategory(id)
      ElMessage.success('删除成功')
      loadCategories()
    } catch (e) {
      if (e.response && e.response.status === 400) {
        ElMessage.error('该分类下有话术，无法删除')
      } else {
        ElMessage.error('删除失败')
      }
    }
  })
}

onMounted(() => {
  loadCategories()
})
</script>
