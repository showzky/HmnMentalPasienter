<template>
  <div class="min-h-screen flex items-center justify-center bg-[#181A20] font-sans">
    <div class="absolute top-6 left-6">
<router-link
  to="/"
  class="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-500 via-indigo-600 to-purple-600
         text-white font-semibold rounded-full shadow-xl transition-all duration-200
         hover:scale-105 hover:from-purple-500 hover:to-blue-600 hover:shadow-2xl focus:outline-none"
>
  <span class="text-xl">🏠</span>
  <span>Return to Main Site</span>
</router-link>

    </div>
    <section class="max-w-3xl w-full p-8 bg-[#23272F] rounded-2xl shadow-2xl border border-slate-700">
      <article
        v-html="htmlContent"
        class="prose prose-xl prose-invert leading-relaxed text-slate-100"
      />
    </section>
  </div>
</template>







<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const htmlContent = ref('Loading...')


const markdownFile = '/TERMS.md'

onMounted(async () => {
  const res = await fetch(markdownFile)
  const md = await res.text()
  htmlContent.value = DOMPurify.sanitize(marked.parse(md))
})
</script>
