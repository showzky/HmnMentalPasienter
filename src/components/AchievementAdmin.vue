<template>
  <section class="achievement-admin">
    <div class="admin-layout">
      <!-- Achievement Creation/Editing Form -->
      <div class="form-panel">
        <h3 class="form-title"><i class="fa fa-trophy"></i> Create / Edit Achievement</h3>
        <div class="form-fields">
          <input v-model="form.title" placeholder="Title" class="input-fancy" />
          <textarea v-model="form.description" placeholder="Description" class="input-fancy" />
          <input type="file" accept=".svg" @change="handleSvgUpload" class="input-fancy-file" />
          <img v-if="svgPreviewUrl" :src="svgPreviewUrl" class="svg-preview" alt="SVG Preview" />
          <div v-if="form.icon && form.icon.startsWith('<svg')" v-html="form.icon" class="svg-preview"></div>

          <select v-model="form.condition_type" class="input-fancy">
            <option disabled value="">Select Condition</option>
            <option value="login_streak">Login Streak</option>
            <option value="active_hours">Active Hours</option>
            <option value="daily_claims">Daily Reward Claims</option>
            <option value="custom">Custom</option>
          </select>
          <input v-if="form.condition_type" v-model.number="form.condition_value"
            :placeholder="conditionPlaceholder(form.condition_type)" class="input-fancy" type="number" min="1" />
          <input v-model="form.rarity" placeholder="Rarity (e.g. common, rare, epic)" class="input-fancy" />
          <input v-model="form.glow_color" placeholder="Glow Color (e.g. #ffeb3b or gold)" class="input-fancy" />

          <div class="form-actions">
            <button @click="submitForm" class="main-action-btn">{{ form.id ? 'Update' : 'Create' }}</button>
            <button v-if="form.id" @click="resetForm" class="reset-btn">Cancel</button>
          </div>
        </div>
      </div>
      <!-- Achievements List -->
      <div class="items-panel">
        <h2 class="panel-title"><i class="fa fa-star"></i> Achievements</h2>
        <div class="achievements-grid">
          <div class="achievement-card" v-for="ach in achievements" :key="ach.id">
            <div class="achievement-icon" v-html="ach.icon"></div>
            <div class="ach-info">
              <div class="ach-title">{{ ach.title }}</div>
              <div class="ach-desc">{{ ach.description }}</div>
              <div class="ach-condition">{{ showCondition(ach) }}</div>
            </div>
            <div class="ach-actions">
              <button class="action-btn edit" @click="startEdit(ach)">✎</button>
              <button class="action-btn delete" @click="deleteAchievement(ach.id)">🗑</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from '@/axios'
export default {
  name: 'AchievementAdmin',
  data() {
    return {
      achievements: [],
      form: {
        id: null,
        title: '',
        description: '',
        icon: '',
        condition_type: '',
        condition_value: 1,
        rarity: '',
        glow_color: ''
      },
      svgPreviewUrl: null,
    }
  },
  methods: {
    async fetchAchievements() {
      const { data } = await axios.get('/all-achievements')
      this.achievements = data
    },
    showCondition(ach) {
      switch (ach.condition_type) {
        case 'login_streak': return `Login streak: ${ach.condition_value} days`;
        case 'active_hours': return `Active: ${ach.condition_value} hours`;
        case 'daily_claims': return `Daily rewards: ${ach.condition_value} days`;
        case 'custom': return 'Custom Condition';
        default: return '';
      }
    },
    conditionPlaceholder(type) {
      switch (type) {
        case 'login_streak': return "Enter days (e.g. 7)";
        case 'active_hours': return "Enter hours (e.g. 10)";
        case 'daily_claims': return "Enter claims (e.g. 5)";
        case 'custom': return "Custom value";
        default: return "";
      }
    },
    startEdit(ach) {
      this.form = { ...ach }
      this.svgPreviewUrl = ach.icon && ach.icon.startsWith('data:image') ? ach.icon : null
    },
    resetForm() {
      this.form = {
        id: null,
        title: '',
        description: '',
        icon: '',
        condition_type: '',
        condition_value: 1
      }
      this.svgPreviewUrl = null
    },
    async submitForm() {
      if (!this.form.title || !this.form.condition_type) return alert("Title & condition required!");
      if (this.form.id) {
        await axios.put(`/achievements/${this.form.id}`, this.form)
      } else {
        await axios.post('/achievements', this.form)
      }
      this.resetForm()
      await this.fetchAchievements()
    },
    async deleteAchievement(id) {
      if (!confirm('Delete this achievement?')) return
      await axios.delete(`/achievements/${id}`)
      await this.fetchAchievements()
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
    this.fetchAchievements()
  }
}
</script>

<style scoped>
.achievement-admin {
  width: 100%;
  height: 100%;
  padding: 1rem;
  font-family: 'Inter', Arial, sans-serif;
}

.admin-layout {
  display: flex;
  gap: 2.2rem;
  align-items: flex-start;
  height: 100%;
}

.form-panel {
  min-width: 325px;
  max-width: 370px;
  width: 100%;
  background: #22263a;
  border-radius: 1.5rem;
  box-shadow: 0 2px 12px 0 rgba(44, 54, 87, .11);
  padding: 2rem 1.3rem 1.2rem 1.3rem;
  position: sticky;
  top: 2rem;
  align-self: flex-start;
}

.form-title {
  font-size: 1.18rem;
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

.input-fancy,
.input-fancy:focus,
.input-fancy:active,
textarea.input-fancy {
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
  background: linear-gradient(90deg, #ffb964 30%, #f26e6e 100%);
  color: #fff;
  font-weight: 700;
  border: none;
  padding: .74em 2.1em;
  border-radius: 1.1em;
  font-size: 1.04rem;
  letter-spacing: .04em;
  box-shadow: 0 1px 6px #ffbb332e;
  cursor: pointer;
  transition: background .14s;
}

.main-action-btn:hover {
  background: linear-gradient(90deg, #f5c876 30%, #ff7878 100%);
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

.items-panel {
  flex: 1 1 0%;
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
  min-width: 0;
}

.panel-title {
  color: #fafbff;
  font-size: 1.28rem;
  font-weight: 800;
  letter-spacing: .04em;
  margin-bottom: 1rem;
  text-align: left;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.2rem;
  max-height: 67vh;
  overflow-y: auto;
  padding-right: .5rem;
}

.achievement-card {
  background: #212538;
  border-radius: 1.1rem;
  padding: 1rem .8rem .7rem .8rem;
  box-shadow: 0 2px 8px #19214415;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 160px;
  position: relative;
}

.achievement-icon {
  width: 38px;
  height: 38px;
  margin-bottom: .7em;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ach-info {
  text-align: center;
}

.ach-title {
  font-size: 1.04rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: .18em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ach-desc {
  font-size: .96em;
  color: #ffa08b;
  margin-bottom: .14em;
}

.ach-condition {
  font-size: .9em;
  color: #bbb;
  font-style: italic;
}

.ach-actions {
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

.action-btn.edit {
  color: #33e388;
}

.action-btn.delete {
  color: #f54c4c;
}

.action-btn:hover {
  background: #26304e;
}

/* Responsive! */
@media (max-width: 1024px) {
  .admin-layout {
    flex-direction: column;
  }

  .form-panel,
  .items-panel {
    max-width: 100%;
  }
}

@media (max-width: 700px) {
  .achievements-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }

  .form-panel {
    padding: 1rem 0.5rem;
  }

  .achievement-admin {
    padding: 0.5rem;
  }
}
</style>