<template>
  <div>
    <h2>Your Purchased Items</h2>
    <div class="badge-list">
      <span
        v-for="item in purchasedItems"
        :key="item.id"
        class="badge-item-wrapper"
      >
        <!-- SVG as Cloudinary URL or base64: render as standalone image -->
        <template v-if="item.icon && (item.icon.endsWith('.svg') || item.icon.startsWith('data:image/svg+xml'))">
          <img
            :src="item.icon"
            class="item-svg-icon"
            alt="SVG Icon"
          />
          <span class="badge-name">{{ item.name }}</span>
          <button class="badge-remove" @click="removeItem(item)">&times;</button>
        </template>
        <!-- Otherwise, render as badge shape -->
        <template v-else>
          <span
            class="badge"
            :class="item.rarity"
            :style="item.glow_color && item.glow_color !== '#cccccc' && item.glow_color !== '#ccc' ? { backgroundColor: item.glow_color } : {}"
          >
            <span class="badge-pill">{{ item.icon }}</span>
            <span class="badge-name">{{ item.name }}</span>
            <button class="badge-remove" @click="removeItem(item)">&times;</button>
          </span>
        </template>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/axios';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
const purchasedItems = ref([]);

const fetchPurchasedItems = async () => {
  const token = localStorage.getItem('access_token');
  const res = await axios.get(`${import.meta.env.VITE_API_URL}/purchased-items`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  purchasedItems.value = res.data;
};

const removeItem = async (item) => {
  const token = localStorage.getItem('access_token');
  await axios.post(`${import.meta.env.VITE_API_URL}/remove-item`, 
    { itemId: item.id },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  await fetchPurchasedItems();
  await auth.fetchFittePoints();
};

onMounted(() => {
  fetchPurchasedItems();
});
</script>

<style scoped>
.badge-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
}
.badge-item-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.badge-icon {
  font-size: 1.3rem;
  margin-right: 0.5rem;
  display: flex;
  align-items: center;
}
.badge-name {
  font-weight: 600;
  margin-right: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.badge-price {
  color: #00c97b;
  font-size: 0.95em;
  margin-right: 0.5rem;
  font-weight: 500;
}
.badge-remove {
  background: none;
  border: none;
  color: #888;
  font-size: 1.1em;
  margin-left: 0.2rem;
  cursor: pointer;
  padding: 0 0.2em;
  border-radius: 50%;
  transition: background 0.2s, color 0.2s;
}
.badge-remove:hover {
  background: #e74c3c22;
  color: #e74c3c;
}
.item-svg-icon {
  width: 140px;
  height: 140px;
  display: inline-block;
  vertical-align: middle;
}
</style>
  