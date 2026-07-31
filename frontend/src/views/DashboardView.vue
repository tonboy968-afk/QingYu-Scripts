<template>
  <div style="padding: 20px;">
    <h1>仪表盘</h1>
    
    <!-- 快捷搜索 -->
    <el-card style="margin-bottom: 20px;">
      <el-input
        v-model="searchKeyword"
        placeholder="输入关键词快速搜索话术..."
        style="width: 300px; margin-right: 10px;"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-statistic title="话术总数" :value="stats.total_scripts || 0" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="分类数" :value="stats.total_categories || 0" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="店铺数" :value="stats.total_stores || 0" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="售后规则数" :value="stats.total_rules || 0" />
      </el-col>
    </el-row>

    <!-- 分类话术数量分布 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <div class="card-header">
          <span>各分类话术数量分布</span>
        </div>
      </template>
      <el-table :data="categoryDistribution" style="width: 100%">
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="count" label="话术数量" width="120" />
      </el-table>
    </el-card>

    <!-- 最近更新的话术 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>最近更新的话术</span>
        </div>
      </template>
      <el-table :data="recentScripts" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="store_name" label="店铺" width="120" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboardStats } from '../api/dashboard.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const stats = ref({})
const categoryDistribution = ref([])
const recentScripts = ref([])
const searchKeyword = ref('')

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/scripts', query: { q: searchKeyword.value } })
  }
}

onMounted(async () => {
  try {
    const res = await getDashboardStats()
    stats.value = res.data || {}
    categoryDistribution.value = res.data?.category_distribution || []
    recentScripts.value = res.data?.recent_scripts || []
  } catch (e) {
    console.error('Failed to fetch dashboard stats', e)
  }
})
</script>
