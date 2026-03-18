<template>
  <!-- Main Content -->
  <main class="admin-content">
    <div class="content-area">
      <!-- Producer-only tabs -->
      <!-- ========== Producer: Events Tab ========== -->
      <section v-if="isOnlyProducer && activeTab === 'content'">
        <div class="event-list-card">
          <div class="existing-events-header">
            <h3>Existing Events</h3>
            <input type="text" :value="searchQuery" @input="$emit('update:searchQuery', $event.target.value)" placeholder="Search Events..." class="search-input" />
          </div>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th style="width: 30px;"></th> <!-- Drag handle column -->
                  <th>Event Name</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th style="width: 100px;">Actions</th>
                </tr>
              </thead>
              <tbody v-if="upcomingEventsData && upcomingEventsData.length" ref="eventsTable" class="events-table">
                <tr v-for="(element, index) in upcomingEventsData" :key="element.id">
                  <td class="drag-handle" style="cursor: grab;">☰</td>
                  <td>{{ element.event_name }}</td>
                  <td>{{ formatDate(element.event_date) }}</td>
                  <td>{{ formatTime(element.event_time) }}</td>
                  <td>
                    <button @click="$emit('deleteEvent', element.id)" class="delete-button">Delete</button>
                  </td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr>
                  <td colspan="5" class="no-events">No events found</td>
                </tr>
              </tbody>
            </table>
          </div>
          
        </div>
        <div class="create-event-card">
          <h3>Create New Event</h3>
          <div class="form-grid">
            <div class="form-group">
              <label for="event-name">Name</label>
              <input 
                type="text" 
                id="event-name" 
                :value="newEvent.event_name" 
                @input="updateNewEventField('event_name', $event.target.value)" 
                placeholder="Event Title" />
            </div>
            <div class="form-group">
              <label for="event-date">Date</label>
              <input 
                type="date" 
                id="event-date" 
                :value="newEvent.event_date" 
                @input="updateNewEventField('event_date', $event.target.value)" />
            </div>
            <div class="form-group">
              <label for="event-time">Time</label>
              <input 
                type="time" 
                id="event-time" 
                :value="newEvent.event_time" 
                @input="updateNewEventField('event_time', $event.target.value)" />
            </div>
            
            <div class="form-group">
              <label for="template_name">Template</label>
              <select 
                id="template_name" 
                :value="newEvent.template_name" 
                @input="updateNewEventField('template_name', $event.target.value)" 
                required>
                <option value="" disabled>Select a Template</option>
                <option value="template1">Template 1 (Image-Focused)</option>
                <option value="template2">Template 2 (Text-Focused)</option>
              </select>
            </div>

          </div>
          <div class="form-group full-width">
            <label for="event-description">Description (Optional)</label>
            <textarea 
              id="event-description" 
              :value="newEvent.event_description" 
              @input="updateNewEventField('event_description', $event.target.value)" 
              placeholder="Short event details..."></textarea>
          </div>
          <div class="form-group full-width file-upload-group">
            <label for="event_image" class="file-upload-label">
              <span>Choose an Image</span>
              <input type="file" id="event_image" @change="$emit('handleImageUpload', $event)" accept="image/*" class="hidden-file-input" />
            </label>
          </div>
          <div class="checkbox-group">
            <label class="custom-checkbox">
              <input 
                type="checkbox" 
                :checked="newEvent.notify_users" 
                @change="updateNewEventField('notify_users', $event.target.checked)" />
              Notify all users
            </label>
          </div>
          <button @click="$emit('createEvent')" class="create-event-button">Create</button>
          <div v-if="createEventMessage" class="form-message" :class="{ success: createEventSuccess, error: !createEventSuccess }">
            {{ createEventMessage }}
          </div>
        </div>
      </section>
      <!-- ========== Producer: Music Tab ========== -->
      <section v-if="isOnlyProducer && activeTab === 'music'" class="music-admin">
        <div class="data-widget">
          <h3>Manage Bangerfabrikken Playlist</h3>
          <table class="playlist-table">
            <thead>
              <tr>
                <th style="width: 30px;"></th>
                <th>Title</th>
                <th>Artist</th>
                <th>SoundCloud URL</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody ref="playlistTable" class="playlist-table">
              <tr v-for="(element, index) in playlist" :key="element.id">
                <td class="drag-handle" style="cursor: grab;">☰</td>
                <td>{{ element.title }}</td>
                <td>{{ element.artist }}</td>
                <td>{{ element.soundcloudUrl }}</td>
                <td>
                  <button class="delete-song" @click="$emit('deleteSong', element.id)">Delete</button>
                  <button class="edit-song" @click="$emit('editSong', element.id)">Edit</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="form-group-music">
            <label>Title</label>
            <input :value="newSong.title" @input="updateNewSongField('title', $event.target.value)" />
          </div>
          <div class="form-group-music">
            <label>Artist</label>
            <input :value="newSong.artist" @input="updateNewSongField('artist', $event.target.value)" />
          </div>
          <div class="form-group-music">
            <label>Cover URL</label>
            <input :value="newSong.cover" @input="updateNewSongField('cover', $event.target.value)" />
          </div>
          <div class="form-group-music">
            <label>SoundCloud URL</label>
            <input :value="newSong.soundcloudUrl" @input="updateNewSongField('soundcloudUrl', $event.target.value)" />
          </div>
          <button @click="$emit('saveSong')" class="create-role-button">
            {{ editingIndex !== null ? 'Update Song' : 'Add Song' }}
          </button>
          <div v-if="playlistMessage" class="form-message" :class="{ success: playlistSuccess, error: !playlistSuccess }">
            {{ playlistMessage }}
          </div>
        </div>
      </section>
      <!-- ========== Admin/Developer Tabs ========== -->
      <template v-if="!isOnlyProducer">
        <!-- Dashboard Tab -->
        <DashboardTab 
          v-if="activeTab === 'dashboard'"
          :upcomingEventsData="upcomingEventsData"
          :widgets="widgets"
        />
        
        <!-- System Info Tab -->
        <SystemTab v-if="activeTab === 'system'" />
        
        <!-- Events Tab -->
        <EventsTab 
          v-if="activeTab === 'content'"
          :searchQuery="searchQuery"
          :upcomingEventsData="upcomingEventsData"
          :newEvent="newEvent"
          :createEventMessage="createEventMessage"
          :createEventSuccess="createEventSuccess"
          @deleteEvent="$emit('deleteEvent', $event)"
          @handleImageUpload="$emit('handleImageUpload', $event)"
          @createEvent="$emit('createEvent')"
          @update:searchQuery="$emit('update:searchQuery', $event)"
          @update:newEvent="$emit('update:newEvent', $event)"
        />
        
        <!-- Music Tab -->
        <MusicTab 
          v-if="activeTab === 'music'"
          :playlist="playlist"
          :newSong="newSong"
          :editingIndex="editingIndex"
          :playlistMessage="playlistMessage"
          :playlistSuccess="playlistSuccess"
          @saveSong="$emit('saveSong')"
          @deleteSong="$emit('deleteSong', $event)"
          @editSong="$emit('editSong', $event)"
          @playlistDragEnd="$emit('playlistDragEnd', $event)"
          @update:newSong="$emit('update:newSong', $event)"
        />
        
        <!-- Shop Items Tab -->
        <ShopTab v-if="activeTab === 'shop'" />
        
        <!-- News Management Tab -->
        <NewsTab v-if="activeTab === 'news'" />
        
        <!-- User Roles Tab -->
        <UsersTab 
          v-if="activeTab === 'users'"
          :userRoles="userRoles"
          :usersList="usersList"
          :userRoleUpdate="userRoleUpdate"
          :availableRoles="availableRoles"
          :updateUserMessage="updateUserMessage"
          :updateUserSuccess="updateUserSuccess"
          :selectedUserRoles="selectedUserRoles"
          :userRoleRemove="userRoleRemove"
          :selectedUserRolesToRemove="selectedUserRolesToRemove"
          :rolesToRemove="rolesToRemove"
          :removeRoleMessage="removeRoleMessage"
          :removeRoleSuccess="removeRoleSuccess"
          :newRole="newRole"
          :createRoleMessage="createRoleMessage"
          :createRoleSuccess="createRoleSuccess"
          @updateUserRole="$emit('updateUserRole')"
          @fetchUserRolesToRemove="$emit('fetchUserRolesToRemove')"
          @removeSelectedRoles="$emit('removeSelectedRoles')"
          @createRole="$emit('createRole')"
          @deleteRole="$emit('deleteRole', $event)"
          @update:userRoleUpdate="$emit('update:userRoleUpdate', $event)"
          @update:userRoleRemove="$emit('update:userRoleRemove', $event)"
          @update:rolesToRemove="$emit('update:rolesToRemove', $event)"
          @update:newRole="$emit('update:newRole', $event)"
        />
        
        <!-- Team Manager Tab -->
        <TeamTab 
          v-if="activeTab === 'team'"
          :teamMembers="teamMembers"
          :defaultAvatar="defaultAvatar"
          :teamMessage="teamMessage"
          :teamSuccess="teamSuccess"
          @saveTeamMember="$emit('saveTeamMember', $event)"
          @deleteTeamMember="$emit('deleteTeamMember', $event)"
          @addNewTeamMember="$emit('addNewTeamMember')"
          @triggerAvatarUpload="$emit('triggerAvatarUpload', $event)"
          @update:teamMembers="$emit('update:teamMembers', $event)"
        />
        
        <!-- Maintenance Settings Tab -->
        <SettingsTab 
          v-if="activeTab === 'settings'"
          :maintenanceMode="maintenanceMode"
          :noticeMaintenanceMode="noticeMaintenanceMode"
          :maintenanceBannerMessage="maintenanceBannerMessage"
          :maintenanceMessage="maintenanceMessage"
          :maintenanceSuccess="maintenanceSuccess"
          :noticeMaintenanceMessage="noticeMaintenanceMessage"
          :noticeMaintenanceSuccess="noticeMaintenanceSuccess"
          @onToggleMaintenance="$emit('onToggleMaintenance')"
          @onToggleNoticeMaintenance="$emit('onToggleNoticeMaintenance')"
          @update:maintenanceMode="$emit('update:maintenanceMode', $event)"
          @update:noticeMaintenanceMode="$emit('update:noticeMaintenanceMode', $event)"
          @update:maintenanceBannerMessage="$emit('update:maintenanceBannerMessage', $event)"
        />
        
        <!-- Changelog Management Tab -->
        <ChangeLogTab
          v-if="activeTab === 'changelog'"
          :newChangelog="newChangelog"
          :changelogEntries="changelogEntries"
          :changelogMessage="changelogMessage"
          :changelogSuccess="changelogSuccess"
          @submitChangelogEntry="$emit('submitChangelogEntry')"
          @deleteChangelogEntry="$emit('deleteChangelogEntry', $event)"
          @update:newChangelog="$emit('update:newChangelog', $event)"
        />
        
        <!-- Achievement Tab -->
        <AchievementTab v-if="activeTab === 'achievements'" :achievements="achievements" />
      </template>
    </div>
  </main>
</template>

<script>
import DashboardTab from './tabs/DashboardTab.vue';
import SystemTab from './tabs/SystemTab.vue';
import EventsTab from './tabs/EventsTab.vue';
import MusicTab from './tabs/MusicTab.vue';
import ShopTab from './tabs/ShopTab.vue';
import NewsTab from './tabs/NewsTab.vue';
import UsersTab from './tabs/UsersTab.vue';
import TeamTab from './tabs/TeamTab.vue';
import SettingsTab from './tabs/SettingsTab.vue';
import ChangeLogTab from './tabs/ChangeLogTab.vue';
import AchievementTab from './tabs/AchievementTab.vue';
import Sortable from 'sortablejs';

export default {
  components: {
    DashboardTab,
    SystemTab,
    EventsTab,
    MusicTab,
    ShopTab,
    NewsTab,
    UsersTab,
    TeamTab,
    SettingsTab,
    ChangeLogTab,
    AchievementTab
  },
  props: {
    displayName: { type: String, default: '' },
    isOnlyProducer: { type: Boolean, default: false },
    activeTab: { type: String, default: 'dashboard' },
    searchQuery: { type: String, default: '' },
    upcomingEventsData: { type: Array, default: () => [] },
    newEvent: { type: Object, default: () => ({ event_name:'', event_date:'', event_time:'', event_description:'', template_name:'', event_image:null, notify_users:false }) },
    playlist: { type: Array, default: () => [] },
    editingIndex: { type: Number, default: null },
    playlistMessage: { type: String, default: '' },
    playlistSuccess: { type: Boolean, default: false },
    createEventMessage: { type: String, default: '' },
    createEventSuccess: { type: Boolean, default: false },
    userRoles: { type: Array, default: () => [] },
    usersList: { type: Array, default: () => [] },
    userRoleUpdate: { type: Object, default: () => ({ selectedUser:'', newRole:'' }) },
    availableRoles: { type: Array, default: () => [] },
    updateUserMessage: { type: String, default: '' },
    updateUserSuccess: { type: Boolean, default: false },
    selectedUserRoles: { type: Array, default: () => [] },
    userRoleRemove: { type: Object, default: () => ({ selectedUser:'' }) },
    selectedUserRolesToRemove: { type: Array, default: () => [] },
    rolesToRemove: { type: Array, default: () => [] },
    removeRoleMessage: { type: String, default: '' },
    removeRoleSuccess: { type: Boolean, default: false },
    newRole: { type: Object, default: () => ({ name:'', badge_icon:'', badge_color:'' }) },
    createRoleMessage: { type: String, default: '' },
    createRoleSuccess: { type: Boolean, default: false },
    teamMembers: { type: Array, default: () => [] },
    defaultAvatar: { type: String, default: '' },
    teamMessage: { type: String, default: '' },
    teamSuccess: { type: Boolean, default: false },
    maintenanceMode: { type: Boolean, default: false },
    noticeMaintenanceMode: { type: Boolean, default: false },
    maintenanceBannerMessage: { type: String, default: '' },
    maintenanceMessage: { type: String, default: '' },
    maintenanceSuccess: { type: Boolean, default: false },
    noticeMaintenanceMessage: { type: String, default: '' },
    noticeMaintenanceSuccess: { type: Boolean, default: false },
    newChangelog: { type: Object, default: () => ({ version:'', date:'', added:'', changed:'' }) },
    changelogEntries: { type: Array, default: () => [] },
    changelogMessage: { type: String, default: '' },
    changelogSuccess: { type: Boolean, default: false },
    widgets: { type: Array, default: () => [] },
    newSong: { type: Object, default: () => ({ title:'', artist:'', cover:'', soundcloudUrl:'' }) },
    achievements: { type: Array, default: () => ([
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
    ]) }
  },
  emits: [
    'createEvent',
    'deleteEvent',
    'handleImageUpload',
    'saveSong',
    'deleteSong',
    'editSong',
    'updateUserRole',
    'fetchUserRolesToRemove',
    'removeSelectedRoles',
    'createRole',
    'deleteRole',
    'saveTeamMember',
    'deleteTeamMember',
    'addNewTeamMember',
    'triggerAvatarUpload',
    'onToggleMaintenance',
    'onToggleNoticeMaintenance',
    'submitChangelogEntry',
    'deleteChangelogEntry',
    'playlistDragEnd',
    'update:searchQuery',
    'update:newEvent',
    'update:newSong',
    'update:userRoleUpdate',
    'update:userRoleRemove',
    'update:rolesToRemove',
    'update:newRole',
    'update:teamMembers',
    'update:maintenanceMode',
    'update:noticeMaintenanceMode',
    'update:maintenanceBannerMessage',
    'update:newChangelog'
  ],
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    formatTime(timeString) {
      return timeString;
    },
    updateNewEventField(field, value) {
      const updatedEvent = { ...this.newEvent, [field]: value };
      this.$emit('update:newEvent', updatedEvent);
    },
    updateNewSongField(field, value) {
      const updatedSong = { ...this.newSong, [field]: value };
      this.$emit('update:newSong', updatedSong);
    }
  },
  watch: {
    activeTab(newTab) {
      if (this.isOnlyProducer && newTab === 'music') {
        this.$nextTick(() => {
          const playlistTable = this.$refs.playlistTable;
          if (playlistTable && !playlistTable._sortable) {
            playlistTable._sortable = new Sortable(playlistTable, {
              swap: true,
              swapClass: 'highlighted',
              animation: 200,
              easing: "cubic-bezier(0.2, 0, 0, 1)",
              ghostClass: 'sortable-ghost',
              dragClass: 'sortable-drag',
              handle: '.drag-handle',
              onEnd: (evt) => {
                this.$emit('playlistDragEnd', evt);
              }
            });
            console.log("Sortable initialized for producer playlist on tab switch");
          }
        });
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.isOnlyProducer && this.activeTab === 'music') {
        const playlistTable = this.$refs.playlistTable;
        if (playlistTable && !playlistTable._sortable) {
          playlistTable._sortable = new Sortable(playlistTable, {
            swap: true,
            swapClass: 'highlighted',
            animation: 200,
            easing: "cubic-bezier(0.2, 0, 0, 1)",
            ghostClass: 'sortable-ghost',
            dragClass: 'sortable-drag',
            handle: '.drag-handle',
            onEnd: (evt) => {
              this.$emit('playlistDragEnd', evt);
            }
          });
          console.log("Sortable initialized for producer playlist table");
        }
      }
    });
  }
}

</script>
