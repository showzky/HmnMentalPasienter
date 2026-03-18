<template>
  <div class="news-page">
    <header class="news-header">
      <div class="header-content">
        <h1>📰 Community News</h1>
        <p class="subtitle">Stay updated with the latest announcements and updates</p>
      </div>
    </header>

    <main class="news-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading news...</p>
      </div>

      <div v-else-if="news.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <h3>No News Yet</h3>
        <p>Check back later for updates!</p>
      </div>

      <div v-else class="news-grid">
        <article
          v-for="(item, i) in news"
          :key="item.id"
          :class="['news-card', { 'latest-news-card': i === 0 }]"
        >
          <div class="news-card-header">
            <h2 class="news-title">{{ item.title }}</h2>
            <time class="news-date" :datetime="item.date">{{ formatDate(item.date) }}</time>
          </div>
          <div
            class="news-content"
            v-html="item.content"
          ></div>
          <button
            class="show-more"
            @click="expandedNews = item"
            v-if="item.content && item.content.length > 300"
          >Show More</button>
          <div class="news-footer">
            <div class="news-meta">
              <span class="read-time">{{ estimateReadTime(item.content) }} min read</span>
            </div>
          </div>
        </article>
      </div>
      <BaseModal v-if="expandedNews" @close="expandedNews = null">
        <h2>{{ expandedNews.title }}</h2>
        <time>{{ formatDate(expandedNews.date) }}</time>
        <div v-html="expandedNews.content"></div>
      </BaseModal>
    </main>
  </div>
</template>

<script>
import axios from '@/axios';
import BaseModal from '@/components/BaseModal.vue';

export default {
  name: 'NewsPage',
  components: { BaseModal },
  data() {
    return {
      news: [],
      loading: true,
      expandedNews: null // Holds the news item to show in modal
    };
  },
  methods: {
    async fetchNews() {
      try {
        this.loading = true;
        const response = await axios.get('/news');
        this.news = response.data;
      } catch (err) {
        console.error('Failed to fetch news:', err);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    estimateReadTime(content) {
      const wordsPerMinute = 200;
      const wordCount = content.replace(/<[^>]*>/g, '').split(/\s+/).length;
      return Math.max(1, Math.ceil(wordCount / wordsPerMinute));
    }
  },
  mounted() {
    this.fetchNews();
  }
};
</script>

<style scoped>
.news-page {
  min-height: 100vh;
  background: #f8fafc;
}

.latest-news-card {
  border: 2px solid #3b82f6; /* Primary blue, matches your header text */
  background: #f0f7ff;
  box-shadow: 0 8px 28px rgba(59,130,246,0.08);
  position: relative;
}

.latest-news-card::after {
  content: 'Latest';
  position: absolute;
  top: 18px; right: 22px;
  background: #3b82f6;
  color: #fff;
  font-size: 0.8rem;
  padding: 0.2em 0.8em;
  border-radius: 999px;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 6px rgba(59,130,246,0.08);
}
.news-header {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
}

.news-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(to right, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.1rem;
  color: #94a3b8;
  margin-top: 1rem;
}

.news-container {
  max-width: 1200px;
  margin: -3rem auto 4rem;
  padding: 0 2rem;
  position: relative;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.news-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.news-card-header {
  padding: 1.5rem 1.5rem 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.news-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0 0 0.5rem;
  font-weight: 600;
  line-height: 1.3;
}

.news-date {
  font-size: 0.875rem;
  color: #64748b;
  display: block;
}

.news-content {
  color: #2e3338;
  font-size: 1rem;
  line-height: 1.6;
  margin: 1rem 0;
  flex-grow: 1;
  max-height: 9.6em; /* 6 lines x 1.6em line-height */
  overflow: hidden;
  position: relative;
  transition: max-height 0.3s cubic-bezier(.4,0,.2,1);
  display: -webkit-box;
  -webkit-line-clamp: 6;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
}

.news-content.expanded {
  max-height: 1000vh;
  overflow-y: visible;
  display: block;
  -webkit-line-clamp: unset;
  -webkit-box-orient: unset;
  text-overflow: unset;
}

.news-content:not(.expanded)::after {
  content: '';
  display: block;
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 2.5rem;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(255,255,255,0), #fff 90%);
}

.news-footer {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.news-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.read-time {
  font-size: 0.875rem;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.read-time::before {
  content: "🕒";
  font-size: 1rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

.empty-state {
  text-align: center;
  padding: 4rem 0;
  color: #64748b;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0 0 0.5rem;
}

.empty-state p {
  color: #64748b;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .news-header {
    padding: 3rem 1.5rem;
  }

  .news-header h1 {
    font-size: 2rem;
  }

  .news-container {
    padding: 0 1rem;
    margin-top: -2rem;
  }

  .news-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .news-card-header {
    padding: 1.25rem 1.25rem 0.5rem;
  }

  .news-content {
    max-height: 160px;
  }

  .news-footer {
    padding: 1rem 1.25rem;
  }
}

.show-more {
  background: none;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 0.5rem;
  margin-left: 1rem;
  align-self: flex-start;
  transition: color 0.2s;
}

.show-more:hover {
  color: #1d4ed8;
  text-decoration: underline;
}
</style>
  