<template>
  <div class="shop-container">
    <!-- Best Practice: Use semantic HTML for accessibility -->
    <header class="shop-header">
      <h1 class="shop-title">Fitte Points Shop</h1>
      <div class="points-balance" aria-live="polite">
        <span class="balance-label">Your Balance:</span>
        <span class="balance-amount">{{ fittePoints }} FP</span>
      </div>
    </header>

    <!-- Tabs for Badges & Themes -->
    <nav class="shop-tabs" role="tablist">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'badge' }"
        @click="activeTab = 'badge'"
        role="tab"
        :aria-selected="activeTab === 'badge'"
      >
        Badges
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'theme' }"
        @click="activeTab = 'theme'"
        role="tab"
        :aria-selected="activeTab === 'theme'"
      >
        Themes
      </button>
    </nav>

    <section class="shop-items" aria-label="Shop Items">
      <article
        class="shop-item"
        v-for="item in filteredItems"
        :key="item.id"
      >
        <div class="item-icon-wrapper">
          <!-- SVG as inline string -->
          <span
            v-if="item.icon && item.icon.startsWith('<svg')"
            v-html="item.icon"
            class="item-svg-icon"
          ></span>
          <!-- SVG as base64 data URL -->
          <img
            v-else-if="item.icon && item.icon.startsWith('data:image/svg+xml')"
            :src="item.icon"
            class="item-svg-icon"
            :alt="item.name + ' icon'"
          />
          <!-- SVG as Cloudinary URL -->
          <img
            v-else-if="item.icon && item.icon.endsWith('.svg') && item.icon.startsWith('https://res.cloudinary.com')"
            :src="item.icon"
            class="item-svg-icon"
            :alt="item.name + ' icon'"
          />
          <!-- Emoji or text fallback -->
          <span v-else class="item-icon" :aria-label="item.name + ' icon'" role="img">
            {{ item.icon || 'Badge' }}
          </span>
        </div>
        <div class="item-content">
          <h2 class="item-name">{{ item.name }}</h2>
          <p class="item-description">{{ item.description }}</p>
          <!-- Best Practice: Separate concerns with clear action handlers -->
          <div class="item-footer">
            <span class="item-price">{{ item.price }} FP</span>
            <button
              class="purchase-btn"
              :disabled="fittePoints < item.price"
              @click="purchaseItem(item)"
              :aria-disabled="fittePoints < item.price"
            >
              Buy
            </button>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import axios from '@/axios';

export default {
  name: 'Shop',
  setup() {
    const auth = useAuthStore();
    const activeTab = ref('badge');
    const defaultGlow = (rarity) => {
    const colors = {
    common: '#aaa',
    rare: '#3498db',
    epic: '#9b59b6',
    legendary: '#f39c12'
  };
  return colors[rarity] || '#aaa';
};
    const items = ref([]);

    const fetchShopItems = async () => {
      try {
        const { data } = await axios.get('/shop-items');
        items.value = data;
      } catch (e) {
        console.error('Error fetching shop items:', e);
      }
    };

    const filteredItems = computed(() => {
      const filtered = items.value.filter(item => item.type === activeTab.value);
      console.log('Shop filteredItems:', filtered);
      return filtered;
    });

    const fittePoints = ref(0);

    const fetchFittePoints = async () => {
      try {
        const { data } = await axios.get('/get-fitte-points');
        fittePoints.value = data.points;
      } catch (e) {
        console.error('Failed to fetch points:', e);
      }
    };

    onMounted(() => {
  fetchFittePoints();
  fetchShopItems();
  });

    // add logic to update points after purchase ;) 
    const purchaseItem = async (item) => {
  try {
    console.log('Purchasing:', item);
    await axios.post('/purchase-item', { itemId: item.id });
    await fetchFittePoints(); // Refresh points after purchase
  } catch (error) {
    const msg = error.response?.data?.msg || 'Purchase failed';
    console.error('Purchase failed:', msg);
    // Optionally show a toast or alert here:
    // alert(msg);
  }
};

    return {
      fittePoints,
      activeTab,
      filteredItems,
      purchaseItem,
      defaultGlow
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Roboto:wght@400;700&display=swap');
@import '@/assets/badges.css';

.shop-container {
  --primary: #ff4081;
  --secondary: #536dfe;
  --accent: #ff9100;
  --bg-color: #1e1e2f;
  --card-bg: #29293d;
  --text: #f5f5f5;
  font-family: 'Press Start 2P', sans-serif;
  background: var(--bg-color);
  color: var(--text);
  max-width: 1000px;
  margin: 2rem auto;
  padding: 1rem;
}

.shop-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--secondary);
}

.shop-title {
  font-size: 2.5rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--primary);
}

.points-balance {
  background: var(--card-bg);
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Roboto', sans-serif;
}

.balance-label {
  opacity: 0.8;
  font-size: 0.9rem;
}

.balance-amount {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--accent);
}

.shop-tabs {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
}

.tab-btn {
  flex: 1;
  padding: 0.75rem;
  background: var(--card-bg);
  border: 2px solid transparent;
  border-radius: 0.75rem;
  cursor: pointer;
  font-family: 'Roboto', sans-serif;
  transition: all 0.3s ease;
}

.tab-btn.active {
  background: var(--primary);
  border-color: var(--accent);
  color: #fff;
}

.tab-btn:hover:not(.active) {
  background: rgba(255,255,255,0.1);
}

.shop-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.shop-item {
  background: var(--card-bg);
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.shop-item:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}

.item-icon-wrapper {
  background: rgba(255,255,255,0.05);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 120px;
}

.item-icon {
  font-size: 3rem;
}

.item-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-family: 'Roboto', sans-serif;
}

.item-name {
  font-size: 1.2rem;
  color: var(--text);
}

.item-description {
  font-size: 0.9rem;
  opacity: 0.8;
  flex: 1;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.item-price {
  font-weight: 600;
  font-family: 'Press Start 2P', sans-serif;
  color: var(--accent);
}

.purchase-btn {
  padding: 0.5rem 1rem;
  background: var(--secondary);
  border: none;
  border-radius: 0.5rem;
  font-family: 'Roboto', sans-serif;
  cursor: pointer;
  transition: background 0.3s;
}

.purchase-btn:hover:not(:disabled) {
  background: var(--accent);
}

.purchase-btn:disabled {
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.5);
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .shop-header {
    flex-direction: column;
    gap: 1rem;
  }
  .shop-tabs {
    flex-direction: column;
  }
}

.item-svg-icon {
  width: 140px;
  height: 140px;
  display: inline-block;
  vertical-align: middle;
}
</style>
