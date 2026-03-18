<template>
  <section class="news-admin">
    <div class="data-widget">
      <h3 class="admin-title">Manage News</h3>
      <form @submit.prevent="saveNews" class="news-form">
        <div class="input-group">
          <input 
            v-model="form.title" 
            placeholder="Enter news title..." 
            required 
            class="title-input"
          />
        </div>
        <div class="editor-container">
<quill-editor 
  v-model:content="form.content" 
  content-type="html"
  :toolbar="toolbarOptions"
  class="quill-editor"
/>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">
            {{ editing ? "Update" : "Add" }} News
          </button>
          <button 
            type="button" 
            v-if="editing" 
            @click="cancelEdit"
            class="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>

      <div class="news-list">
        <div v-for="item in newsItems" :key="item.id" class="news-item">
          <div class="news-item-content">
            <h4 class="news-title">{{ item.title }}</h4>
            <div class="news-body" v-html="item.content"></div>
          </div>
          <div class="news-actions">
            <button @click="editNews(item)" class="btn btn-edit">
              <span class="btn-icon">✏️</span> Edit
            </button>
            <button @click="deleteNews(item.id)" class="btn btn-delete">
              <span class="btn-icon">🗑️</span> Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import axios from 'axios';
import { useAuthStore } from '@/stores/authStore';

export default {
  components: { QuillEditor },
  data() {
    return {
      newsItems: [],
      form: { id: null, title: "", content: "", date: "" },
      editing: false,
      toolbarOptions: [
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'header': [1, 2, 3, false] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'font': [] }],
        [{ 'align': [] }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['link', 'image'],
        ['clean']
      ]
    }
  },
  methods: {
async saveNews() {
  try {
    const auth = useAuthStore();
    const token = auth.token;
    if (!token) {
      console.warn('Missing token — cannot post news.');
      return;
    }

    const payload = {
      title: this.form.title,
      content: this.form.content,
      date: new Date().toISOString().slice(0, 10)
    };

    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    };

    if (this.editing) {
      await axios.put(`${import.meta.env.VITE_API_URL}/news/${this.form.id}`, payload, config);
    } else {
      await axios.post(`${import.meta.env.VITE_API_URL}/news`, payload, config);
    }

    await this.fetchNews();
    this.resetForm();
  } catch (err) {
    console.error('Failed to save news:', err.response?.data || err.message);
  }
  },

  editNews(item) {
    this.form = { ...item };
    this.editing = true;
  },

async deleteNews(id) {
  if (!id) return console.error('No news ID provided');

  const auth = useAuthStore();
  const token = auth.token;
  if (!token) {
    console.warn('Missing token — cannot delete news.');
    return;
  }

  try {
    await axios.delete(`${import.meta.env.VITE_API_URL}/news/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    await this.fetchNews();
  } catch (err) {
    console.error('Failed to delete news:', err.response?.data || err.message);
  }
  },

  cancelEdit() {
    this.resetForm();
  },

resetForm() {
  this.form = { id: null, title: "", content: "" };
  this.editing = false;
},
async fetchNews() {
  try {

        const auth = useAuthStore();
        const headers = {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
          'Expires': '0'
        };

        if (auth.token) { // Use auth store here too
          headers.Authorization = `Bearer ${auth.token}`;
        }

    const response = await axios.get(`${import.meta.env.VITE_API_URL}/news`, { headers });
    console.log('Fetched news:', response.data);
    this.newsItems = Array.isArray(response.data) ? response.data : [];
  } catch (err) {
    console.error('Failed to fetch news:', err.response?.data || err.message);
  }
}


  },
  mounted() {
    this.fetchNews();
  }
}
</script>

<style scoped>
.news-admin {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.data-widget {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.admin-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-weight: 600;
}

.news-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.input-group {
  width: 100%;
}

.title-input {
  width: 100%;
  padding: 0.8rem 1rem;
  font-size: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.3s ease;
  outline: none;
}

.title-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.editor-container {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
}

.quill-editor {
  height: 200px;
  background: white;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #e2e8f0;
  color: #64748b;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

.news-list {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.news-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.news-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.news-item-content {
  flex: 1;
}

.news-title {
  font-size: 1.2rem;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.news-body {
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.5;
}

.news-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit {
  background: #22c55e;
  color: white;
}

.btn-edit:hover {
  background: #16a34a;
}

.btn-delete {
  background: #ef4444;
  color: white;
}

.btn-delete:hover {
  background: #dc2626;
}

.btn-icon {
  font-size: 1.1rem;
}

/* Quill Editor Overrides */
:deep(.ql-toolbar) {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border: none;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

:deep(.ql-container) {
  border: none;
  font-size: 1rem;
}

:deep(.ql-editor) {
  min-height: 200px;
  font-family: inherit;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .news-admin {
    padding: 1rem;
  }

  .data-widget {
    padding: 1.5rem;
  }

  .news-item {
    flex-direction: column;
  }

  .news-actions {
    width: 100%;
    justify-content: flex-end;
    margin-top: 1rem;
  }
}
</style>