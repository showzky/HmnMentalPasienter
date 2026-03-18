<template>
  <section class="shop-admin">
    <div class="dashboard-layout">
      <!-- LEFT COLUMN: FORM PANEL -->
      <div class="form-panel">
        <h3 class="form-title">
          <i class="fa fa-plus-circle"></i> Create / Edit Item
        </h3>
        <div class="form-fields">
          <input v-model="form.name" placeholder="Name" class="input-fancy" />
          <input type="file" accept=".svg" @change="handleSvgUpload" class="input-fancy-file"/>
          <img v-if="svgPreviewUrl" :src="svgPreviewUrl" class="svg-preview" alt="SVG Preview" />
          <div v-if="form.icon && form.icon.startsWith('<svg')" v-html="form.icon" class="svg-preview"></div>
          <select v-model="form.type" class="input-fancy">
            <option value="badge">Badge</option>
            <option value="theme">Theme</option>
          </select>
          <input type="number" v-model.number="form.price" placeholder="Price" class="input-fancy"/>
          <input v-model="form.icon" placeholder="Icon (e.g. 🥇)" class="input-fancy"/>
          <template v-if="form.type === 'badge'">
            <select v-model="form.rarity" class="input-fancy">
              <option value="common">Common</option>
              <option value="rare">Rare</option>
              <option value="epic">Epic</option>
              <option value="legendary">Legendary</option>
            </select>
            <input v-model="form.glow_color" type="color" class="input-fancy" />
            <textarea v-model="form.description" placeholder="Description" class="input-fancy"></textarea>
          </template>
          <div class="form-actions">
            <button @click="submitForm" class="main-action-btn">{{ form.id ? 'Update' : 'Create' }}</button>
            <button v-if="form.id" @click="resetForm" class="reset-btn">Cancel</button>
          </div>
          <BadgePreview
            v-if="form.type === 'badge'"
            :icon="form.icon"
            :rarity="form.rarity"
            :glowColor="form.glow_color || defaultGlow(form.rarity)"
            :description="form.description"
          />
        </div>
      </div>
      <!-- CENTER COLUMN: ITEMS PANEL -->
      <div class="items-panel">
        <div class="shop-header-row">
          <h2 class="shop-title">
            <i class="fa fa-shopping-cart"></i> Manage Shop Items
          </h2>
          <div class="search-row">
            <input
              v-model="searchTerm"
              placeholder="Search badges/themes by name..."
              class="input-fancy"
              @input="filterItems"
            />
            <select v-model="filterType" class="input-fancy" @change="filterItems">
              <option value="">All Types</option>
              <option value="badge">Badge</option>
              <option value="theme">Theme</option>
            </select>
          </div>
        </div>
        <div class="items-grid-container">
          <div class="items-grid">
            <div
              class="item-card"
              v-for="item in filteredItems"
              :key="item.id"
            >
              <div class="item-icon-wrapper">
                <span
                  v-if="item.icon && item.icon.startsWith('<svg')"
                  v-html="item.icon"
                  class="item-svg-icon"
                ></span>
                <img
                  v-else-if="item.icon && item.icon.startsWith('data:image/svg+xml')"
                  :src="item.icon"
                  class="item-svg-icon"
                  :alt="item.name + ' icon'"
                />
                <img
                  v-else-if="item.icon && item.icon.endsWith('.svg')"
                  :src="item.icon"
                  class="item-svg-icon"
                  :alt="item.name + ' icon'"
                />
                <span v-else class="item-icon" :aria-label="item.name + ' icon'" role="img">
                  {{ item.icon || 'Badge' }}
                </span>
              </div>
              <div class="card-info">
                <div class="card-title">{{ item.name }}</div>
                <div class="card-type type-pill" :class="item.type">{{ item.type }}</div>
                <div class="card-price price-pill">{{ item.price }}</div>
              </div>
              <div class="card-actions">
                <button class="action-btn edit" @click="startEdit(item)">✎</button>
                <button class="action-btn delete" @click="deleteItem(item.id)">🗑</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Achievements Section Below Shop Items -->

  </section>
</template>

<script>
import axios from '@/axios'
import BadgePreview from './BadgePreview.vue'


export default {
  name: 'ShopAdmin',
  components: {
    BadgePreview,

  },
  data() {
    return {
      shopItems: [],
      filteredItems: [],
      searchTerm: '',
      filterType: '',
      form: {
        id: null,
        name: '',
        type: 'badge',
        price: 0,
        icon: '',
        rarity: 'common',
        glow_color: '#cccccc',
        description: ''
      },
      svgPreviewUrl: null,
      icon: '',
      achievements: [
        {
          id: 1,
          title: '10 Hours Active',
          description: 'Be active for 10 hours!',
          svg: '<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="30" fill="#FFD700" stroke="#E5C100" stroke-width="4"/><text x="32" y="40" text-anchor="middle" font-size="24" fill="#222">10h</text></svg>',
          achieved: false
        },
        {
          id: 2,
          title: 'SVG URL Example',
          description: 'This uses an SVG URL.',
          svg: '/assets/achievements/example.svg',
          achieved: true
        }
      ]
    }
  },
  methods: {
    async fetchShopItems() {
      const { data } = await axios.get('/shop-items')
      this.shopItems = data.map(item => ({
        ...item,
        glow_color: item.glow_color || '#cccccc'
      }))
      this.filterItems()
    },
    filterItems() {
      this.filteredItems = this.shopItems.filter(item => {
        const nameMatch = item.name.toLowerCase().includes(this.searchTerm.toLowerCase());
        const typeMatch = this.filterType === '' || item.type === this.filterType;
        return nameMatch && typeMatch;
      });
    },
    defaultGlow(rarity) {
      const colors = {
        common: '#aaa',
        rare: '#3498db',
        epic: '#9b59b6',
        legendary: '#f39c12'
      }
      return colors[rarity] || '#aaa'
    },
    startEdit(item) {
      this.form = {
        ...item,
        glow_color: item.glow_color || '#cccccc'
      }
    },
    resetForm() {
      this.form = {
        id: null,
        name: '',
        type: 'badge',
        price: 0,
        icon: '',
        rarity: 'common',
        glow_color: '#cccccc',
        description: ''
      };
      this.svgPreviewUrl = null;
    },
    async submitForm() {
      if (this.form.type === 'badge' && (!this.form.glow_color || this.form.glow_color.trim() === '')) {
        this.form.glow_color = '#cccccc'
      }
      if (this.form.id) {
        await axios.put(`/shop-items/${this.form.id}`, this.form)
      } else {
        await axios.post('/shop-items', this.form)
      }
      this.resetForm()
      await this.fetchShopItems()
    },
    async deleteItem(id) {
      if (!confirm('Delete this item?')) return
      await axios.delete(`/shop-items/${id}`)
      await this.fetchShopItems()
    },
    async handleSvgUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      const formData = new FormData();
      formData.append('svg_file', file);

      try {
        const { data } = await axios.post('/upload-svg', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.form.icon = data.url;
        this.svgPreviewUrl = data.url;
      } catch (e) {
        alert('SVG upload failed: ' + (e.response?.data?.msg || e.message));
      }
    },
  },
  mounted() {
    this.fetchShopItems()
  }
}
</script>

<style scoped>


/* Layout Core */
.shop-admin {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 80vh;
  background: #1a1e26;
  border-radius: 2rem;
  box-shadow: 0 8px 32px 0 rgba(31,38,135,0.18);
  margin: 2.5rem auto;
  padding: 2.5rem 2.5rem 2.5rem 2.5rem;
  max-width: 1400px;
  width: 100%;
  box-sizing: border-box;
}

.dashboard-layout {
  display: flex;
  gap: 2.5rem;
  width: 100%;
  align-items: flex-start;
  justify-content: stretch;
}

.form-panel,
.items-panel,
.achievement-panel {
  background: #23273a;
  border-radius: 1.5rem;
  box-shadow: 0 2px 12px 0 rgba(44,54,87,.14);
  padding: 2rem 1.3rem 1.5rem 1.3rem;
  display: flex;
  flex-direction: column;
  min-width: 340px;
  max-width: 400px;
  width: 100%;
  align-self: flex-start;
}

/* Make items-panel take more width */
.items-panel {
  flex: 1 1 0%;
  min-width: 380px;
  max-width: 650px;
  margin: 0 1.4rem;
  background: #20222c;
  padding: 2rem 2rem 1.5rem 2rem;
}

/* Achievements style */
.achievement-panel {
  min-width: 340px;
  max-width: 400px;
  background: #21252f;
  padding: 2rem 1.3rem 1.5rem 1.3rem;
}

/* ---- Form panel ---- */
.form-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 1.7rem;
  text-align: left;
  letter-spacing: .04em;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.input-fancy, .input-fancy:focus, .input-fancy:active, textarea.input-fancy {
  border: none;
  border-radius: .85em;
  background: #1e222f;
  color: #e9eafc;
  padding: .7em 1em;
  font-size: 1rem;
  box-shadow: 0 1px 6px 0 #1a1e2830;
  outline: none;
  margin-bottom: .1em;
  transition: box-shadow .15s;
}
.input-fancy:focus {
  box-shadow: 0 2px 10px #4588ff44;
}
.input-fancy-file {
  padding: .5em .1em .5em 0;
  color: #fff;
}
textarea.input-fancy {
  min-height: 66px;
  resize: vertical;
}
.svg-preview {
  width: 38px;
  height: 38px;
  background: #222;
  border-radius: 1em;
  box-shadow: 0 0 8px 1px #1e90ff22;
  padding: .28em;
  margin: .07em 0;
  display: inline-block;
  vertical-align: middle;
}
.form-actions {
  display: flex;
  gap: 1em;
  align-items: center;
  margin-top: .5em;
}
.main-action-btn {
  background: linear-gradient(90deg, #5670ff 40%, #4e3be6 100%);
  color: #fff;
  font-weight: 700;
  border: none;
  padding: .74em 2.1em;
  border-radius: 1.1em;
  font-size: 1.05rem;
  letter-spacing: .04em;
  box-shadow: 0 1px 6px #2d55e640;
  cursor: pointer;
  transition: background .14s;
}
.main-action-btn:hover {
  background: linear-gradient(90deg, #4364e8 30%, #6754ff 100%);
}
.reset-btn {
  background: #2e333e;
  color: #bfc8e7;
  font-weight: 500;
  border: none;
  padding: .74em 2.1em;
  border-radius: 1.1em;
  font-size: 1.03rem;
  cursor: pointer;
  transition: background .14s;
}
.reset-btn:hover {
  background: #353a44;
}

/* ---- Items Panel (grid) ---- */
.shop-header-row {
  display: flex;
  flex-direction: column;
  gap: .75rem;
}
.shop-title {
  color: #fafbff;
  font-size: 1.65rem;
  font-weight: 800;
  letter-spacing: .04em;
  margin-bottom: .3rem;
  text-align: left;
}
.search-row {
  display: flex;
  gap: .9rem;
  align-items: center;
  margin-bottom: .3rem;
}
.items-grid-container {
  max-height: 65vh;
  overflow-y: auto;
  padding-right: .5rem;
}
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 1.2rem;
}
.item-card {
  background: #212538;
  border-radius: 1.1rem;
  padding: 1rem 1rem .6rem 1rem;
  box-shadow: 0 2px 8px #1921441b;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  min-height: 190px;
  position: relative;
}
.item-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 34px;
}
.item-svg-icon {
  width: 38px;
  height: 38px;
  background: #222;
  border-radius: 1em;
  box-shadow: 0 0 8px 1px #1e90ff22;
  padding: .28em;
  margin: .07em 0;
  display: inline-block;
  vertical-align: middle;
}
.item-icon {
  font-size: 2rem;
  display: inline-block;
}
.card-info {
  text-align: center;
  margin-top: .6em;
  margin-bottom: .5em;
}
.card-title {
  font-size: 1.09rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: .2em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-type, .card-price {
  display: inline-block;
  margin: .18em .4em .18em 0;
}
.type-pill {
  display: inline-block;
  padding: .20em .75em;
  border-radius: 1em;
  font-size: .93em;
  font-weight: 500;
  background: #34486c;
  color: #fff;
  text-transform: capitalize;
}
.type-pill.badge { background: #32499b; }
.type-pill.theme { background: #238d6b; }
.price-pill {
  background: #302e6a;
  color: #ffd700;
  padding: .23em .8em;
  border-radius: 1em;
  font-weight: 700;
  font-size: .93em;
  letter-spacing: .03em;
}
.card-actions {
  display: flex;
  gap: .4em;
  margin-top: .25em;
  justify-content: center;
}
.action-btn {
  border: none;
  outline: none;
  background: none;
  margin: 0 .15em;
  padding: .4em .7em;
  border-radius: .6em;
  font-size: 1.05rem;
  cursor: pointer;
  transition: background .15s;
}
.action-btn.edit { color: #33e388; }
.action-btn.delete { color: #f54c4c; }
.action-btn:hover {
  background: #26304e;
}

/* ---- Responsive Layouts ---- */
@media (max-width: 1280px) {
  .shop-admin {
    padding: 1.2rem;
    max-width: 100vw;
  }
  .dashboard-layout {
    gap: 1rem;
  }
  .items-panel { padding: 1.2rem; }
}

@media (max-width: 1024px) {
  .dashboard-layout {
    flex-direction: column;
    gap: 2rem;
  }
  .items-panel, .achievement-panel, .form-panel {
    max-width: 100%;
    min-width: 0;
    width: 100%;
    align-self: stretch;
    margin: 0;
  }
}

@media (max-width: 700px) {
  .shop-admin {
    padding: 0.5rem 0.2rem 2rem 0.2rem;
    border-radius: 0.7rem;
  }
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 0.7rem;
  }
  .form-panel, .items-panel, .achievement-panel {
    padding: 1rem 0.5rem;
  }
}

/* ----- Panel Spacer (optional) ----- */
.panel-spacer {
  width: 36px;
  min-width: 16px;
  flex-shrink: 0;
  display: block;
}

/* Make sure footer stays at bottom */
footer, .footer {
  flex-shrink: 0;
}

</style>
