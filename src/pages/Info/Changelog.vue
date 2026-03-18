<template>
  <div class="changelog-page" id="changelog">
    <h1 class="page-title">Changelog 📝</h1>
    <div v-if="changelogs.length > 0">
      <div
        v-for="changelog in changelogs"
        :key="changelog.id"
        class="changelog-entry"
      >
        <div
          class="entry-header"
          :class="{ expanded: expandedIds.includes(changelog.id) }"
          @click="toggleEntry(changelog.id)"
        >
          <span class="version-badge">{{ changelog.version }}</span>
          <span class="date">({{ changelog.date }})</span>
          <span class="toggle-icon">
            <svg
              :class="{ rotated: expandedIds.includes(changelog.id) }"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </span>
          
        </div>

        <transition name="fade">
          <div v-if="expandedIds.includes(changelog.id)" class="entry-content">
            <div class="change-block" v-if="changelog.added && changelog.added.length > 0">
              <h3><span class="icon">➕</span> Added</h3>
              <ul>
                <li v-for="item in changelog.added" :key="item">{{ item }}</li>
              </ul>
            </div>
            <div class="change-block" v-if="changelog.changed && changelog.changed.length > 0">
              <h3><span class="icon">♻️</span> Changed</h3>
              <ul>
                <li v-for="item in changelog.changed" :key="item">{{ item }}</li>
              </ul>
            </div>
            <div class="change-block" v-if="changelog.fixed && changelog.fixed.length > 0">
              <h3><span class="icon">🛠️</span> Fixed</h3>
              <ul>
                <li v-for="item in changelog.fixed" :key="item">{{ item }}</li>
              </ul>
            </div>
            <div class="change-block" v-if="changelog.removed && changelog.removed.length > 0">
              <h3><span class="icon">➖</span> Removed</h3>
              <ul>
                <li v-for="item in changelog.removed" :key="item">{{ item }}</li>
              </ul>
            </div>
          </div>
        </transition>
      </div>
    </div>
    <div v-else>
      <p>No changelog entries found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Changelog',
  data() {
    return {
      changelogs: [],
      expandedIds: []
    };
  },
  async mounted() {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/changelog`);
      console.log('API Response:', response.data);
      this.changelogs = response.data;
    } catch (error) {
      console.error('Failed to fetch changelog', error);
    }
  },
  methods: {
    toggleEntry(id) {
      if (this.expandedIds.includes(id)) {
        this.expandedIds = this.expandedIds.filter(entryId => entryId !== id);
      } else {
        this.expandedIds.push(id);
      }
    }
  }
};
</script>

<style scoped>
/* Global Color Variables - Updated */
:root {
    --bg-color: #f8f9fa; /* Lighter background */
    --text-color: #343a40; /* Darker grey text */
    --card-bg: #ffffff; /* White cards */
    --primary-accent: #e83e8c; /* A slightly bolder pink */
    --secondary-text: #6c757d; /* Muted grey for dates/less important text */
    --border-color: #e9ecef; /* Light grey border */
}

.dark-mode {
    --bg-color: #212529; /* Dark background */
    --text-color: #dee2e6; /* Light grey text */
    --card-bg: #343a40; /* Dark grey cards */
    --primary-accent: #fd7e14; /* An orange accent for dark mode */
    --secondary-text: #adb5bd; /* Lighter grey in dark mode */
    --border-color: #495057; /* Darker grey border */
}

/* Apply base styles to body (consider if this should be global or within the component) */
body {
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: 'Inter', sans-serif; /* Modern sans-serif font */
    transition: background 0.3s ease, color 0.3s ease;
    padding: 20px;
    line-height: 1.6; /* Improved readability */
}

.changelog-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.page-title {
    text-align: center;
    font-size: 2.8rem;
    letter-spacing: 0.5px;
    margin-bottom: 2rem;
    position: relative;
    display: inline-block;
    padding-bottom: 0.5rem;
    color: var(--text-color);
  }

 .dark-mode .changelog-entry {
    background: rgba(52, 58, 64, 0.6);
  }

  .page-title::after {
    content: "";
    display: block;
    width: 60%;
    height: 3px;
    margin: 0.5rem auto 0;
    background: linear-gradient(90deg, var(--primary-accent), transparent);
    border-radius: 10px;
  }

  .changelog-entry {
    background: rgba(255, 255, 255, 0.6); /* light glass effect */
    border: 1px solid var(--border-color);
    border-left: 5px solid var(--primary-accent);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    padding: 1.2rem 1rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
    backdrop-filter: blur(6px);
  }

  .changelog-entry:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }

  .entry-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    padding: 0.7rem 0;
    user-select: none;
  }

  .version-badge {
    background: var(--primary-accent);
    color: rgb(0, 0, 0);
    padding: 0.35rem 0.9rem;
    border-radius: 9999px;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 80px;
  }

  .date {
    color: var(--secondary-text);
    font-size: 0.9rem;
    margin-left: auto;
    margin-right: 1rem;
  }

.toggle-icon {
  font-size: 1.2rem;
  color: var(--secondary-text);
  transition: transform 0.3s ease;
}

.entry-content {
    overflow: hidden;
    transition: all 0.4s ease;
  }

.toggle-icon svg.rotated {
    transform: rotate(180deg);
  }

.expanded .toggle-icon {
  transform: rotate(180deg);
}

.change-block {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.change-block h3 {
    font-size: 1.25rem;
    color: var(--text-color);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
  }

.change-block h3 .icon {
  margin-right: 0.5rem;
  font-size: 1.5rem;
  color: var(--primary-accent);
}

.change-block ul {
  padding-left: 1.5rem;
  list-style: disc;
}

.change-block li {
    margin-bottom: 0.5rem;
    color: var(--text-color);
    line-height: 1.5;
  }

code {
    background: var(--border-color); /* Use border color for code background */
    padding: 3px 7px;
    border-radius: 5px;
    font-family: 'Fira Code', monospace; /* Monospace font */
    font-size: 0.9em;
    color: var(--text-color);
}

.dark-mode code {
    background: rgba(255, 255, 255, 0.15); /* Lighter background in dark mode */
    color: var(--text-color);
}

/* Fade Transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Responsive tweaks */
@media (max-width: 768px) {
    .page-title {
        font-size: 2rem;
    }

    .changelog-entry {
        padding: 1.2rem;
    }

    .version-badge {
        padding: 4px 10px;
        font-size: 0.85rem;
        margin-right: 10px;
        min-width: 60px;
    }

    .date {
        font-size: 0.9rem;
    }

    .change-block h3 {
        font-size: 1.2rem;
    }

    .change-block h3 .icon {
         font-size: 1.3rem;
         margin-right: 8px;
    }

    .change-block ul {
        padding-left: 20px;
    }

    .change-block li {
        margin-bottom: 0.7rem;
    }
}

</style>