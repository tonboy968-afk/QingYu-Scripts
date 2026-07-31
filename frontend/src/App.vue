<template>
  <el-container style="height:100vh">
    <el-aside width="200px" style="background:#fff;border-right:1px solid #eee">
      <el-menu :default-active="activeIndex" @select="handleSelect" background-color="#fff" text-color="#333" active-text-color="#409eff">
        <el-menu-item index="/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/scripts">话术管理</el-menu-item>
        <el-menu-item index="/categories">分类管理</el-menu-item>
        <el-menu-item index="/stores">店铺管理与售后规则</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="display:flex;align-items:center;border-bottom:1px solid #eee;padding:0 20px;height:60px !important;">
        <span style="font-weight:bold;font-size:18px">多店铺客服话术管理系统</span>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeIndex = ref('/dashboard')

const handleSelect = (index) => {
  activeIndex.value = index
  router.push(index)
}
</script>

<style>
body { margin: 0; padding: 0; }
</style>
