<script setup>
defineProps({
  subtitle: {
    type: String,
    default: '关键词检索 · 统计可视化 · 影响力排序 · 智能综述'
  }
})
</script>

<template>
  <header class="site-header">
    <div class="container header-inner">
      <div class="brand">
        <div class="brand-logo">P</div>
        <div class="brand-text">
          <h1>PubMed 科研情报分析平台</h1>
          <p>{{ subtitle }}</p>
        </div>
      </div>
      <div class="header-actions">
        <span class="tech-chip">Vue 3</span>
        <a
          class="source-badge"
          href="https://pubmed.ncbi.nlm.nih.gov/"
          target="_blank"
          rel="noopener"
        >
          数据来源：NCBI PubMed
        </a>
      </div>
    </div>
  </header>
</template>
