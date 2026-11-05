<script setup>
defineProps({
  keyword: { type: String, default: '' },
  sourceUrl: { type: String, default: '' },
  fromCache: { type: Boolean, default: false },
  elapsedSeconds: { type: Number, default: 0 }
})
</script>

<template>
  <section class="result-head">
    <h2>
      检索结果：<span class="kw-highlight">{{ keyword }}</span>
    </h2>
    <div class="result-head-meta">
      <span class="cache-badge" :class="fromCache ? 'is-cache' : 'is-live'">
        {{ fromCache ? '⚡ 本地缓存' : '🛰 实时抓取' }}
        <template v-if="elapsedSeconds > 0">· {{ elapsedSeconds.toFixed(1) }}s</template>
      </span>
      <a class="inline-link" :href="sourceUrl" target="_blank" rel="noopener">
        在 PubMed 查看原始检索结果 →
      </a>
    </div>
  </section>
</template>
