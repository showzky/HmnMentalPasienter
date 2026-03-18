<template>
    <aside class="admin-sidebar">
        <nav>
          <ul>
            <template v-if="!isOnlyProducer">
              <!-- Full admin/developer view -->
              <!-- CORE -->
              <li>
                <div class="group-header" @click="toggleGroup('core')" :aria-expanded="open.core">
                  Core
                  <span class="chevron" :class="{ open: open.core }">▾</span>
                </div>
                <ul v-show="open.core" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='system' }" @click.prevent="$emit('set-active', 'system')">System</a>
                  </li>
                </ul>
              </li>
              <!-- CONTENT -->
              <li>
                <div class="group-header" @click="toggleGroup('content')" :aria-expanded="open.content">
                  Content
                  <span class="chevron" :class="{ open: open.content }">▾</span>
                </div>
                <ul v-show="open.content" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='content' }" @click.prevent="$emit('set-active', 'content')">Events</a>
                  </li>
                  <li>
                    <a href="#" :class="{ active: activeTab==='shop' }" @click.prevent="$emit('set-active', 'shop')">Shop Items</a>
                  </li>
                  <li>
                    <a href="#" :class="{ active: activeTab==='achievements' }" @click.prevent="$emit('set-active', 'achievements')">Achievements</a>
                  </li>
                  <li v-if="isAdminOrDeveloper">
                    <a href="#" :class="{ active: activeTab==='news' }" @click.prevent="$emit('set-active', 'news')">News</a>
                  </li>
                  <li>
                    <a href="#" :class="{ active: activeTab === 'changelog' }" @click.prevent="$emit('set-active', 'changelog')">Changelog</a>
                  </li>
                </ul>
              </li>
              <!-- USERS -->
              <li>
                <div class="group-header" @click="toggleGroup('users')" :aria-expanded="open.users">
                  Users
                  <span class="chevron" :class="{ open: open.users }">▾</span>
                </div>
                <ul v-show="open.users" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='users' }" @click.prevent="$emit('set-active', 'users')">User List</a>
                  </li>
                  <li>
                    <a href="#" :class="{ active: activeTab==='team' }" @click.prevent="$emit('set-active', 'team')">Team Manager</a>
                  </li>
                </ul>
              </li>
              <!-- EXTRAS -->
              <li>
                <div class="group-header" @click="toggleGroup('extras')" :aria-expanded="open.extras">
                  Extras
                  <span class="chevron" :class="{ open: open.extras }">▾</span>
                </div>
                <ul v-show="open.extras" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='music' }" @click.prevent="$emit('set-active', 'music')">Music</a>
                  </li>
                  <li>
                    <a href="#" :class="{ active: activeTab==='settings' }" @click.prevent="$emit('set-active', 'settings')">Settings</a>
                  </li>
                </ul>
              </li>
            </template>
            <template v-else>
              <!-- Producer-only view (Events + Music + Dashboard) -->
              <li>
                <div class="group-header" @click="toggleGroup('core')" :aria-expanded="open.core">
                  Core
                  <span class="chevron" :class="{ open: open.core }">▾</span>
                </div>
                <ul v-show="open.core" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='dashboard' }" @click.prevent="$emit('set-active', 'dashboard')">Dashboard</a>
                  </li>
                </ul>
              </li>
              <li>
                <div class="group-header" @click="toggleGroup('content')" :aria-expanded="open.content">
                  Content
                  <span class="chevron" :class="{ open: open.content }">▾</span>
                </div>
                <ul v-show="open.content" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='content' }" @click.prevent="$emit('set-active', 'content')">Events</a>
                  </li>
                </ul>
              </li>
              <li>
                <div class="group-header" @click="toggleGroup('extras')" :aria-expanded="open.extras">
                  Extras
                  <span class="chevron" :class="{ open: open.extras }">▾</span>
                </div>
                <ul v-show="open.extras" class="group-list">
                  <li>
                    <a href="#" :class="{ active: activeTab==='music' }" @click.prevent="$emit('set-active', 'music')">Music</a>
                  </li>
                </ul>
              </li>
            </template>
          </ul>
        </nav>
      </aside>
</template>

<script>
export default {
  props: [
    'activeTab',
    'isOnlyProducer',
    'isAdminOrDeveloper',
    'open'
  ],
  emits: ['toggle-group', 'set-active'],
  methods: {
    toggleGroup(group) {
      this.$emit('toggle-group', group);
    }
  }
};
</script>
