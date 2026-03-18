<template>
  <div>
    <div v-if="!isLoading" class="admin-body-container">
      <!-- Sidebar Navigation -->
      <AdminSidebar
        :activeTab="activeTab"
        :userRoles="userRoles"
        :open="open"
        :isOnlyProducer="isOnlyProducer"
        :isAdminOrDeveloper="isAdminOrDeveloper"
        @set-active="setActive"
        @toggle-group="toggleGroup"
      />
      
      <!-- Main Content Area -->
      <div class="admin-main-content">
        <AdminHeader :displayName="displayName" />
        <AdminContent
          :displayName="displayName"
          :isOnlyProducer="isOnlyProducer"
          :activeTab="activeTab"
          :searchQuery="searchQuery"
          :upcomingEventsData="upcomingEventsData"
          :newEvent="newEvent"
          :playlist="playlist"
          :editingIndex="editingIndex"
          :playlistMessage="playlistMessage"
          :playlistSuccess="playlistSuccess"
          :createEventMessage="createEventMessage"
          :createEventSuccess="createEventSuccess"
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
          :teamMembers="teamMembers"
          :defaultAvatar="defaultAvatar"
          :teamMessage="teamMessage"
          :teamSuccess="teamSuccess"
          :maintenanceMode="maintenanceMode"
          :noticeMaintenanceMode="noticeMaintenanceMode"
          :maintenanceBannerMessage="maintenanceBannerMessage"
          :maintenanceMessage="maintenanceMessage"
          :maintenanceSuccess="maintenanceSuccess"
          :noticeMaintenanceMessage="noticeMaintenanceMessage"
          :noticeMaintenanceSuccess="noticeMaintenanceSuccess"
          :newChangelog="newChangelog"
          :changelogEntries="changelogEntries"
          :changelogMessage="changelogMessage"
          :changelogSuccess="changelogSuccess"
          :widgets="widgets"
          @createEvent="createEvent"
          @deleteEvent="deleteEvent"
          @handleImageUpload="handleImageUpload"
          @saveSong="saveSong"
          @deleteSong="deleteSong"
          @editSong="editSong"
          @updateUserRole="updateUserRole"
          @fetchUserRolesToRemove="fetchUserRolesToRemove"
          @removeSelectedRoles="removeSelectedRoles"
          @createRole="createRole"
          @deleteRole="deleteRole"
          @saveTeamMember="saveTeamMember"
          @deleteTeamMember="deleteTeamMember"
          @addNewTeamMember="addNewTeamMember"
          @triggerAvatarUpload="triggerAvatarUpload"
          @onToggleMaintenance="onToggleMaintenance"
          @onToggleNoticeMaintenance="onToggleNoticeMaintenance"
          @submitChangelogEntry="submitChangelogEntry"
          @deleteChangelogEntry="deleteChangelogEntry"
          @update:searchQuery="searchQuery = $event"
          @update:newEvent="newEvent = $event"
          @update:playlist="playlist = $event"
          @update:newSong="newSong = $event"
          @playlistDragEnd="onPlaylistDragEnd"
          @update:userRoleUpdate="userRoleUpdate = $event"
          @update:userRoleRemove="userRoleRemove = $event"
          @update:rolesToRemove="rolesToRemove = $event"
          @update:newRole="newRole = $event"
          @update:teamMembers="teamMembers = $event"
          @update:maintenanceMode="maintenanceMode = $event"
          @update:noticeMaintenanceMode="noticeMaintenanceMode = $event"
          @update:maintenanceBannerMessage="maintenanceBannerMessage = $event"
          @update:newChangelog="newChangelog = $event"
        />
      </div>
    </div>
    <div v-else>Loading Management Panel...</div>
  </div>
</template>
<script>
import '@/components/admin/assets/admin.css';
import { useAuthStore } from '@/stores/authStore';
import axios from '@/axios'; 
import { useWebSocket } from '@/composables/useWebSocket';
import { useMotion } from '@vueuse/motion';
import { ref, onMounted } from 'vue';
import ShopAdmin from '../components/ShopAdmin.vue';
import Sortable from 'sortablejs';

import AdminSidebar from '../components/admin/AdminSidebar.vue';
import AdminHeader from '../components/admin/AdminHeader.vue';
import AdminContent from '../components/admin/AdminContent.vue';

export default {
  name: 'Management',
  components: { 
    ShopAdmin,
    AdminSidebar,
    AdminHeader,
    AdminContent
  },
  data() {
    return {
      
      activeTab: 'dashboard',
      isLoading: true,
      searchQuery: '',
      //sidebar dropdown
      open: {
        core: true,
        content: true,
        users: false,
        extras: false
      },
      // Team Manager
      teamMembers: [],
      teamMessage: '',
      teamSuccess: false,
      defaultAvatar: 'https://picsum.photos/200/200',

      // Maintenance Mode
      maintenanceMode: false,
      maintenanceMessage: '',
      maintenanceSuccess: false,

      // Notice Maintenance Mode
      noticeMaintenanceMode: false,
      noticeMaintenanceMessage: '',
      noticeMaintenanceSuccess: false,
      maintenanceBannerMessage: '',

      // Widgets
      widgets: [
        {
          id: 'latest-activity',
          title: 'Latest Activity',
          description: 'Recent updates and happenings on the site.',
          activityItems: [],
        },
        {
          id: 'upcoming-events',
          title: 'Upcoming Events',
          description: 'Never miss out on friend gatherings.',
          eventItems: [],
        }
      ],

      // Users & Roles
      userRoleUpdate: { selectedUser: '', newRole: '' },
      userRoleRemove: { selectedUser: '' },
      usersList: [],
      availableRoles: [],
      updateUserMessage: '',
      updateUserSuccess: false,
      selectedUserRoles: [],
      selectedUserRolesToRemove: [],
      rolesToRemove: [],
      removeRoleMessage: '',
      removeRoleSuccess: false,
      newRole: { name: '', badge_icon: '', badge_color: '' },
      createRoleMessage: '',
      createRoleSuccess: false,

      // Events
      upcomingEventsData: [],
      newEvent: {
        event_name: '',
        event_date: '',
        event_time: '',
        event_description: '',
        template_name: '',
        event_image: null,
        notify_users: false,
      },
      createEventMessage: '',
      createEventSuccess: false,

      // Music
      playlist: [],
      newSong: { title: '', artist: '', cover: '', soundcloudUrl: '' },
      playlistMessage: '',
      playlistSuccess: false,
      editingIndex: null,
      isLoadingSongs: true,

      // Changelog
      newChangelog: {
        version: '',
        date: '',
        added: '',
        changed: ''
      },
      changelogMessage: '',
      changelogSuccess: false,
      changelogEntries: [],
    };
  },

  computed: {
    auth() {
      return useAuthStore();
    },
    canAccessManagement() {
      return ['developer', 'admin', 'producer'].some(role => this.userRoles.includes(role));
    },
    isProducer() {
      return this.userRoles.includes('producer');
    },
    displayName() {
      return this.auth.user?.username || 'Admin User';
    },
    filteredEvents() {
      if (!Array.isArray(this.upcomingEventsData)) return [];
      const query = this.searchQuery.toLowerCase();
      return this.upcomingEventsData.filter(event =>
        event.event_name.toLowerCase().includes(query)
      );
    },
    userRoles() {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        return user?.roles?.map(role => role.name.toLowerCase()) || [];
      } catch {
        return [];
      }
    },
    canManageSongs() {
      return ['developer', 'admin', 'producer'].some(role => this.userRoles.includes(role));
    },
    currentSong() {
      if (!this.playlist.length) return undefined;
      return this.playlist[this.editingIndex ?? 0];
    },
    isOnlyProducer() {
      return (
        this.userRoles.includes('producer') &&
        !this.userRoles.includes('admin') &&
        !this.userRoles.includes('developer')
      );
    },
    isAdminOrDeveloper() {
      return this.userRoles.includes('admin') || this.userRoles.includes('developer');
    },
  },

  methods: {
    setActive(tab) {
      this.activeTab = tab;
    },
    toggleGroup(groupName) {
      this.open[groupName] = !this.open[groupName];
    },
    onDragEnd(evt) {
    console.log('New event order:', this.filteredEvents);
    // Optional: Save the new order here
  },
  onPlaylistDragEnd(evt) {
  // 1) Update local array order
  if (evt.oldIndex !== evt.newIndex) {
    console.log(`Moving song from position ${evt.oldIndex} to ${evt.newIndex}`);
    const moved = this.playlist.splice(evt.oldIndex, 1)[0];
    this.playlist.splice(evt.newIndex, 0, moved);
    
    // Immediately update position properties on the songs
    this.playlist.forEach((song, index) => {
      song.position = index;
    });
    
    console.log('Updated playlist order in memory:', this.playlist.map(s => `${s.title}:${s.position}`));
  }

  // 2) Build payload (id + new position)
  const newOrder = this.playlist.map((song, index) => ({
    id: song.id,
    position: index
  }));
  
  console.log('Saving new order to backend:', newOrder);

  axios.put('/playlist/reorder', { songs: newOrder })
    .then(res => {
      this.playlistMessage = 'Playlist order updated!';
      this.playlistSuccess = true;
      console.log('Backend response after reorder:', res.data);

      // Ensure the local playlist matches the backend response
      if (res.data && res.data.songs && Array.isArray(res.data.songs)) {
        // Sort songs by position to ensure they're in the right order
        const orderedSongs = [...res.data.songs].sort((a, b) => a.position - b.position);
        console.log('Sending to carousel:', orderedSongs.map(s => `${s.title}:${s.position}`));
        
        // 3) Dispatch event with the complete ordered song array
        window.dispatchEvent(new CustomEvent('playlist-order-changed', {
          detail: orderedSongs
        }));
      }
    })
    .catch(err => {
      console.error('Error saving playlist order:', err);
      this.playlistMessage = 'Failed to save new order.';
      this.playlistSuccess = false;
    })
    .finally(() => {
      setTimeout(() => this.playlistMessage = '', 3000);
    });
},


    // ---------------- MAINTENANCE ----------------
    fetchMaintenanceStatus() {
      axios.get('/maintenance-status')
        .then(res => {
          this.maintenanceMode = res.data.maintenance_mode === 'on';
          this.noticeMaintenanceMode = res.data.notice_maintenance_mode === 'on';
        })
        .catch(err => console.error('Failed to fetch maintenance status:', err));
    },
    onToggleMaintenance() {
      axios.post('/maintenance', {
        mode: this.maintenanceMode ? 'on' : 'off'
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(() => {
        this.maintenanceMessage = 'Maintenance mode updated.';
        this.maintenanceSuccess = true;
      })
      .catch(error => {
        console.error('Error toggling maintenance mode:', error);
        this.maintenanceMessage = 'Failed to update maintenance mode.';
        this.maintenanceSuccess = false;
      })
      .finally(() => {
        setTimeout(() => {
          this.maintenanceMessage = '';
        }, 3000);
      });
    },

    onToggleNoticeMaintenance() {
      const message = this.maintenanceBannerMessage.trim();
      console.log('Sending maintenance update:', {
        mode: this.noticeMaintenanceMode ? 'on' : 'off',
        message: message
      });
      
      axios.post('/notice-maintenance', {
        mode: this.noticeMaintenanceMode ? 'on' : 'off',
        message: message
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(res => {
        console.log('Maintenance update response:', res.data);
        this.noticeMaintenanceMessage = 'Notice maintenance mode updated.';
        this.noticeMaintenanceSuccess = true;
      })
      .catch(error => {
        console.error('Error toggling notice maintenance mode:', error);
        this.noticeMaintenanceMessage = 'Failed to update notice maintenance mode. Please try again later.';
        this.noticeMaintenanceSuccess = false;
      })
      .finally(() => {
        setTimeout(() => this.noticeMaintenanceMessage = '', 3000);
      });
    },

    // ---------------- USERS ----------------
    fetchUsersList() {
      axios.get('/users')
        .then(res => this.usersList = res.data.users)
        .catch(err => console.error('Error fetching users:', err));
    },
    fetchRoles() {
      axios.get('/roles')
        .then(res => {
          this.availableRoles = res.data.roles;
          console.log('Fetched roles:', this.availableRoles); // Debug log
        })
        .catch(err => {
          console.error('Error fetching roles:', err);
          this.availableRoles = [];
        });
    },
    updateUserRole() {
      axios.put('/update-user-roles', {
        user_id: this.userRoleUpdate.selectedUser,
        role_ids: [this.userRoleUpdate.newRole]
      })
      .then(res => {
        this.updateUserMessage = res.data.msg;
        this.updateUserSuccess = true;
      })
      .catch(err => {
        console.error('Error updating user role:', err);
        this.updateUserMessage = err.response?.data?.msg || 'Failed to update role';
        this.updateUserSuccess = false;
      })
      .finally(() => {
        setTimeout(() => this.updateUserMessage = '', 3000);
      });
    },
    removeSelectedRoles() {
      if (!this.userRoleRemove.selectedUser || !this.rolesToRemove.length) {
        this.removeRoleMessage = 'Select a user and at least one role to remove.';
        this.removeRoleSuccess = false;
        return;
      }

      const requests = this.rolesToRemove.map(roleId => {
        const role = this.selectedUserRolesToRemove.find(r => r.id === roleId);
        return axios.put('/demote-user', {
          user_id: this.userRoleRemove.selectedUser,
          role_to_remove: role?.name
        });
      });

      Promise.all(requests)
        .then(() => {
          this.removeRoleMessage = 'Roles removed.';
          this.removeRoleSuccess = true;
          this.fetchUserRolesToRemove();
          this.rolesToRemove = [];
        })
        .catch(err => {
          console.error('Error removing roles:', err);
          this.removeRoleMessage = 'Failed to remove one or more roles.';
          this.removeRoleSuccess = false;
        })
        .finally(() => {
          setTimeout(() => this.removeRoleMessage = '', 3000);
        });
    },
    fetchUserRolesToRemove() {
      axios.get('/users')
        .then(res => {
          const user = res.data.users.find(u => u.id === parseInt(this.userRoleRemove.selectedUser));
          this.selectedUserRolesToRemove = user?.roles || [];
        })
        .catch(err => console.error('Error loading user roles:', err));
    },
    createRole() {
      axios.post('/roles', this.newRole)
        .then(res => {
          this.createRoleMessage = res.data.msg;
          this.createRoleSuccess = true;
          this.newRole = { name: '', badge_icon: '', badge_color: '' };
          // Fetch the updated roles list
          this.fetchRoles();
        })
        .catch(err => {
          console.error('Error creating role:', err);
          this.createRoleMessage = err.response?.data?.msg || 'Error creating role.';
          this.createRoleSuccess = false;
        })
        .finally(() => {
          setTimeout(() => this.createRoleMessage = '', 3000);
        });
    },
    deleteRole(roleId) {
      if (!confirm('Delete this role?')) return;
      axios.delete(`/roles/${roleId}`)
        .then(() => this.fetchRoles())
        .catch(err => console.error('Error deleting role:', err));
    },

    // ---------------- EVENTS ---------------- 
    fetchUpcomingEvents() {
      axios.get('/events', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      })
      .then(res => {
        this.upcomingEventsData = Array.isArray(res.data.events) ? res.data.events : [];
      })
      .catch(err => console.error('Error fetching events:', err));
    },
    createEvent() {
      const form = new FormData();
      Object.entries(this.newEvent).forEach(([key, value]) => {
        if (value !== null) form.append(key, value);
      });

      axios.post('/events', form, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(() => {
        this.createEventMessage = 'Event created!';
        this.createEventSuccess = true;
        this.fetchUpcomingEvents();
        this.newEvent = {
          event_name: '',
          event_date: '',
          event_time: '',
          event_description: '',
          template_name: '',
          event_image: null,
          notify_users: false,
        };
      })
      .catch(err => {
        console.error('Error creating event:', err.response?.data || err);
        this.createEventMessage = err.response?.data?.msg || 'Error creating event.';
        this.createEventSuccess = false;
      })
      .finally(() => setTimeout(() => this.createEventMessage = '', 3000));
    },
    deleteEvent(id) {
      if (!confirm('Delete this event?')) return;
      axios.delete(`/events/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      })
      .then(() => this.fetchUpcomingEvents())
      .catch(err => {
        console.error('Delete event failed:', err);
        alert('Error deleting event.');
      });
    },
    formatDate(d) {
      const date = new Date(d);
      return date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
    },
    formatTime(t) {
      return t.split(':').slice(0, 2).join(':');
    },
    handleImageUpload(e) {
      this.newEvent.event_image = e.target.files[0];
    },

    // ---------------- MUSIC ----------------
    fetchPlaylist() {
      console.log('Management: Fetching playlist from backend');
      axios.get('/playlist')
        .then(res => {
          console.log('Management: Received playlist data:', res.data);
          
          if (!res.data || !res.data.songs || !Array.isArray(res.data.songs)) {
            console.error('Management: Invalid playlist data format', res.data);
            this.playlistMessage = 'Error loading playlist - invalid data format';
            this.playlistSuccess = false;
            return;
          }
          
          // Sort by position to ensure consistent order
          this.playlist = [...res.data.songs].sort((a, b) => a.position - b.position);
          console.log('Management: Sorted playlist:', this.playlist.map(s => `${s.title}:${s.position}`));
        })
        .catch(err => {
          console.error('Playlist fetch error:', err);
          this.playlistMessage = 'Error loading playlist';
          this.playlistSuccess = false;
        })
        .finally(() => {
          this.isLoadingSongs = false;
        });
    },
    saveSong() {
      const api = this.editingIndex !== null
        ? axios.put(`/playlist/${this.playlist[this.editingIndex].id}`, this.newSong)
        : axios.post('/playlist', this.newSong);

      api.then(() => {
        this.playlistMessage = this.editingIndex !== null ? 'Song updated!' : 'Song added!';
        this.playlistSuccess = true;
        this.resetForm();
        this.fetchPlaylist();
      })
      .catch(err => {
        console.error('Save song error:', err);
        this.playlistMessage = 'Error saving song.';
        this.playlistSuccess = false;
      })
      .finally(() => setTimeout(() => this.playlistMessage = '', 3000));
    },
    resetForm() {
      this.newSong = { title: '', artist: '', cover: '', soundcloudUrl: '' };
      this.editingIndex = null;
    },
    editSong(id) {
      const index = this.playlist.findIndex(song => song.id === id);
      if (index === -1) return;
      
      this.newSong = { ...this.playlist[index] };
      this.editingIndex = index;
    },
    deleteSong(id) {
      const index = this.playlist.findIndex(song => song.id === id);
      if (index === -1) return;
      
      const song = this.playlist[index];
      if (!confirm(`Delete "${song.title}"?`)) return;
      
      axios.delete(`/playlist/${song.id}`)
        .then(() => {
          this.playlistMessage = 'Song deleted!';
          this.playlistSuccess = true;
          this.fetchPlaylist();
        })
        .catch(err => {
          console.error('Delete song error:', err);
          this.playlistMessage = 'Failed to delete song.';
          this.playlistSuccess = false;
        })
        .finally(() => setTimeout(() => this.playlistMessage = '', 3000));
    },

    // Team Manager Methods
    fetchTeamMembers() {
      axios.get('/team-members')
        .then(res => this.teamMembers = res.data.team_members)
        .catch(err => console.error('Error fetching team members:', err));
    },
    saveTeamMember(member) {
  const isNew = !member.id;

  const hasImage = typeof member.avatar === 'object'; // File object

  const endpoint = isNew ? '/team-members' : `/team-members/${member.id}`;
  const method = isNew ? 'post' : 'put';

  let payload, headers;

  if (hasImage) {
    payload = new FormData();
    Object.entries(member).forEach(([key, value]) => {
      payload.append(key, value);
    });
    headers = {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`
    };
  } else {
    payload = member;
    headers = {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`
    };
  }

  axios[method](endpoint, payload, { headers })
    .then(() => {
      this.teamMessage = isNew ? 'Team member added!' : 'Team member updated!';
      this.teamSuccess = true;
      this.fetchTeamMembers();
    })
    .catch(err => {
      console.error('❌ Error saving team member:', err);
      this.teamMessage = 'Failed to save team member.';
      this.teamSuccess = false;
    })
    .finally(() => {
      setTimeout(() => this.teamMessage = '', 3000);
    });
},

    addNewTeamMember() {
      this.teamMembers.push({
        id: null,
        name: '',
        title: '',
        bio: '',
        avatar: null
      });
    },
    triggerAvatarUpload(memberId) {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.onchange = (e) => this.handleAvatarUpload(e, memberId);
      input.click();
    },
    handleAvatarUpload(event, memberId) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('avatar', file);
      formData.append('member_id', memberId);

      axios.post('/team-members/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(res => {
        const member = this.teamMembers.find(m => m.id === memberId);
        if (member) member.avatar = res.data.avatar_url;
        this.teamMessage = 'Avatar updated successfully!';
        this.teamSuccess = true;
      })
      .catch(err => {
        console.error('Error uploading avatar:', err);
        this.teamMessage = 'Failed to upload avatar.';
        this.teamSuccess = false;
      })
      .finally(() => {
        setTimeout(() => this.teamMessage = '', 3000);
      });
    },

    deleteTeamMember(memberId) {
  // Remove from UI immediately
  this.teamMembers = this.teamMembers.filter(m => m.id !== memberId);

  // If the member exists in the backend, delete from server
  if (memberId) {
    axios.delete(`/team-members/${memberId}`)
      .then(() => {
        this.teamMessage = 'Team member deleted!';
        this.teamSuccess = true;
        this.fetchTeamMembers(); // Refresh list
      })
      .catch(err => {
        console.error('Error deleting team member:', err);
        this.teamMessage = 'Failed to delete team member.';
        this.teamSuccess = false;
      })
      .finally(() => {
        setTimeout(() => this.teamMessage = '', 3000);
      });
  }
},

    async submitChangelogEntry() {
  try {
    const entry = {
      version: this.newChangelog.version,
      date: this.newChangelog.date,
      changes: {
        Added: this.newChangelog.added.split('\n').filter(line => line.trim() !== ''),
        Changed: this.newChangelog.changed.split('\n').filter(line => line.trim() !== ''),
      },
    };
    await this.addChangeLogEntry(entry); // Ensure this matches the method name
    this.changelogMessage = 'Changelog entry added successfully!';
    this.changelogSuccess = true;

    // Reset the form
    this.newChangelog = { version: '', date: '', added: '', changed: '' };
  } catch (error) {
    console.error('Failed to submit changelog entry:', error);
    this.changelogMessage = 'Failed to add changelog entry.';
    this.changelogSuccess = false;
  } finally {
    setTimeout(() => (this.changelogMessage = ''), 3000);
  }
},
  async fetchChangelogEntries() {
    try {
      const response = await axios.get('/changelog');
      this.changelogEntries = response.data;
    } catch (error) {
      console.error('Failed to fetch changelog entries:', error);
    }
  },

  async deleteChangelogEntry(id) {
    if (!confirm('Are you sure you want to delete this changelog entry?')) return;

    try {
      await axios.delete(`/changelog/${id}`);
      this.changelogEntries = this.changelogEntries.filter(entry => entry.id !== id);
      alert('Changelog entry deleted successfully!');
    } catch (error) {
      console.error('Failed to delete changelog entry:', error);
      alert('Failed to delete changelog entry.');
    }
  },
  async addChangeLogEntry(entry) {
    try {
      await axios.post('/changelog', entry);
      alert('Changelog entry added successfully!');
    } catch (error) {
      console.error('Failed to add changelog entry:', error);
      alert('Failed to add changelog entry.');
    }
  },

  },

  mounted() {
    if (!localStorage.getItem('access_token')) {
      return this.$router.push('/login');
    }

    if (!this.canAccessManagement) {
      this.$router.push('/');
      return;
    }

    this.fetchMaintenanceStatus();
    this.fetchUsersList();
    this.fetchRoles();
    this.fetchUpcomingEvents();
    this.fetchPlaylist();
    this.fetchTeamMembers();
    this.fetchChangelogEntries();
    
    if (this.auth.user?.id && this.socket) {
      this.socket.emit('setUserId', this.auth.user.id);
    }

    axios.get('/dashboard/latest-activity')
      .then(res => {
        const widget = this.widgets.find(w => w.id === 'latest-activity');
        if (widget) widget.activityItems = res.data.latest_activity;
      })
      .catch(err => console.error('Dashboard activity error:', err))
      .finally(() => this.isLoading = false);
    
    if (this.isOnlyProducer) {
      this.activeTab = 'content';
    }

    // Initialize sortable after data is loaded and DOM is updated
    // Note: We don't initialize Sortable here anymore since it's handled in watch.activeTab
  },

  watch: {
  activeTab(newTab) {
    if (newTab === 'users') {
      this.fetchRoles(); // Refresh roles when switching to users tab
    }

    // No need to initialize Sortable here anymore as it's handled in component lifecycle or using event bus
  }
},



  setup() {
    const snackBar = ref(null);
    const { socket } = useWebSocket();

    const initSortable = (element, items, updateCallback) => {
      if (!element) return;

      new Sortable(element, {
        animation: 200,
        easing: "cubic-bezier(0.2, 0, 0, 1)",
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        onStart: () => {
          document.body.style.cursor = 'grabbing';
        },
        onEnd: (evt) => {
          document.body.style.cursor = '';
          const newItems = [...items];
          const [movedItem] = newItems.splice(evt.oldIndex, 1);
          newItems.splice(evt.newIndex, 0, movedItem);
          updateCallback(newItems);
        }
      });
    };

    return { 
      snackBar, 
      socket,
      initSortable
    };
  }
};
</script>

<style scoped>

</style>

