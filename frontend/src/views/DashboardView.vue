<template>
  <div>
    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 24px;">
      <el-col :span="6">
        <el-card shadow="hover" style="text-align: center;">
          <div style="font-size: 32px; font-weight: bold; color: #3b82f6;">{{ stats.total_scripts || 0 }}</div>
          <div style="color: #64748b; margin-top: 8px;">话术总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" style="text-align: center;">
          <div style="font-size: 32px; font-weight: bold; color: #10b981;">{{ stats.total_categories || 0 }}</div>
          <div style="color: #64748b; margin-top: 8px;">分类数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" style="text-align: center;">
          <div style="font-size: 32px; font-weight: bold; color: #f59e0b;">{{ stats.total_stores || 0 }}</div>
          <div style="color: #64748b; margin-top: 8px;">店铺数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" style="text-align: center;">
          <div style="font-size: 32px; font-weight: bold; color: #8b5cf6;">{{ stats.total_rules || 0 }}</div>
          <div style="color: #64748b; margin-top: 8px;">售后规则数</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分类话术数量分布 & 最近更新 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>各分类话术数量分布</span>
            </div>
          </template>
          <el-table :data="categoryDistribution" style="width: 100%" size="small">
            <el-table-column prop="name" label="分类名称" />
            <el-table-column prop="count" label="话术数量" width="120" align="right">
              <template #default="scope">
                <el-tag :type="scope.row.count > 5 ? 'primary' : 'info'" size="small">{{ scope.row.count }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最近更新的话术</span>
            </div>
          </template>
          <el-table :data="recentScripts" style="width: 100%" size="small">
            <el-table-column prop="title" label="标题" show-overflow-tooltip />
            <el-table-column prop="category_name" label="分类" width="120" />
            <el-table-column prop="updated_at" label="更新时间" width="160" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboardStats } from '../api/dashboard.js'

const stats = ref({})
const categoryDistribution = ref([])
const recentScripts = ref([])

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

<style scoped>
.card-header {
  font-weight: 600;
  color: #0f172a;
}
</style>
