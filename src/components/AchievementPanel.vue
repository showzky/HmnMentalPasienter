<template>
  <div class="achievements-panel">
    <!-- Add tabs -->
    <div class="achievement-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- Show achievements based on active tab -->
    <div class="achievements-grid">
      <Achievement
        v-for="ach in filteredAchievements"
        :key="ach.id"
        :svg="ach.svg"
        :title="ach.title"
        :description="ach.description"
        :achieved="ach.achieved"
        :rarity="ach.rarity"
        :glow-color="ach.glow_color"
        :unlocked-at="ach.unlocked_at"
      />
    </div>
  </div>
</template>

<script>
import axios from '@/axios'
import Achievement from './Achievement.vue';

export default {
  components: { Achievement },
  data() {
    return {
      achievements: [],         // Site achievements (user-specific)
      clickerAchievements: [],  // Clicker game achievements (with unlock status for user)
      activeTab: 'site',
      tabs: [
        { id: 'site', name: 'Site Achievements' },
        { id: 'clicker', name: 'Clicker Game Achievements' }
      ]
    }
  },
  computed: {
    filteredAchievements() {
      if (this.activeTab === 'site') {
        // Exclude clicker achievements from site tab
        return this.achievements.filter(a => (a.category || '').toLowerCase() !== 'clicker');
      } else {
        // Only include clicker achievements in clicker tab
        return this.clickerAchievements.filter(a => (a.category || '').toLowerCase() === 'clicker');
      }
    }
  },
  methods: {
    async fetchAchievements() {
      try {
        // 1. Fetch site (user) achievements
        const { data: siteAchievements } = await axios.get('/user/achievements');
        this.achievements = siteAchievements.map(a => ({
          id: a.id,
          title: a.title,
          description: a.description,
          svg: a.svg || a.icon,
          achieved: a.achieved,
          rarity: a.rarity,
          glow_color: a.glow_color,
          unlocked_at: a.unlocked_at,
          category: a.category || 'site'
        }));

        // 2. Fetch clicker game achievements
        const { data: clickerAchievements } = await axios.get('/clicker-achievements');
        this.clickerAchievements = clickerAchievements.map(a => ({
          id: a.id,
          title: a.title,
          description: a.description,
          svg: a.svg || a.icon,
          achieved: a.achieved || false,
          rarity: a.rarity || 'common',
          glow_color: a.glow_color || '#ff61c2',
          unlocked_at: a.unlocked_at,
          category: a.category || 'clicker'
        }));
      } catch (e) {
        console.error('Could not fetch achievements:', e);
      }
    }
  },
  mounted() {
    this.fetchAchievements();
  }
}
</script>


<style scoped>
.achievements-panel {
  width: 100%;
}

.achievement-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
  padding-bottom: 0.5rem;
}

.tab-button {
  background: none;
  border: none;
  color: var(--text-color, #000);
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 1rem;
  opacity: 0.7;
  transition: all 0.3s ease;
  position: relative;
}

.tab-button:hover {
  opacity: 1;
}

.tab-button.active {
  opacity: 1;
  font-weight: 600;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  right: 0;
  height: 2px;
  background: #ff61c2;
  border-radius: 2px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}
</style>
