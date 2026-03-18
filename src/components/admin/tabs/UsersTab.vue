<template>
  <section v-if="userRoles.includes('admin') || userRoles.includes('developer')">
    <!-- Admin widgets row: displays widgets side by side -->
    <div class="admin-widgets-row">
      <div class="data-widget">
        <h3>Update User Role</h3>
        <form @submit.prevent="$emit('updateUserRole')">
          <div class="form-group">
            <label for="user-select">Select User</label>
            <select 
              id="user-select" 
              :value="userRoleUpdate.selectedUser"
              @change="updateUserRoleUpdate('selectedUser', $event.target.value)">
              <option value="" disabled>Select a user</option>
              <option v-for="user in usersList" :key="user.id" :value="user.id">
                {{ user.username ? user.username + ', ' + user.email : user.email }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="role-select">Select Role/Rank</label>
            <select 
              id="role-select" 
              :value="userRoleUpdate.newRole"
              @change="updateUserRoleUpdate('newRole', $event.target.value)">
              <option value="" disabled>Select a role</option>
              <option v-for="role in availableRoles" :key="role.id" :value="role.id">
                {{ role.name }}
              </option>
            </select>
          </div>
          <button type="submit" class="update-role-button">Update Role</button>
        </form>
        <div v-if="updateUserMessage" class="form-message" :class="{ success: updateUserSuccess, error: !updateUserSuccess }">
          {{ updateUserMessage }}
        </div>
        <div v-if="selectedUserRoles && selectedUserRoles.length > 0" class="current-roles-container">
          <h4>Current Roles:</h4>
          <span v-for="role in selectedUserRoles" 
                :key="role.id" 
                class="role-badge" 
                :class="role.name.toLowerCase()" 
                :style="{ backgroundColor: role.badge_color }">
            <i v-if="role.badge_icon" :class="role.badge_icon"></i>
            {{ role.name }}
          </span>
        </div>
        <div v-else-if="userRoleUpdate.selectedUser">
          <p>No roles assigned to this user yet.</p>
        </div>
      </div>
      <div class="data-widget">
        <h3>Demote (Remove) User Roles</h3>
        <form @submit.prevent="$emit('removeSelectedRoles')">
          <div class="form-group">
            <label for="user-select-remove">Select User</label>
            <select
              id="user-select-remove"
              :value="userRoleRemove.selectedUser"
              @change="onUserRoleRemoveChange($event.target.value)"
            >
              <option value="" disabled>Select a user</option>
              <option v-for="user in usersList" :key="user.id" :value="user.id">
                {{ user.username ? user.username + ', ' + user.email : user.email }}
              </option>
            </select>
          </div>
          <div v-if="selectedUserRolesToRemove && selectedUserRolesToRemove.length > 0">
            <label>Current Roles:</label>
            <div class="checkbox-group-vertical">
              <label
                v-for="role in selectedUserRolesToRemove"
                :key="role.id"
                class="custom-checkbox"
              >
                <input
                  type="checkbox"
                  :value="role.id"
                  :checked="rolesToRemove.includes(role.id)"
                  @change="toggleRoleToRemove(role.id)"
                />
                {{ role.name }}
              </label>
            </div>
          </div>
          <div v-else-if="userRoleRemove.selectedUser">
            <p>No roles assigned to this user or none found.</p>
          </div>
          <button type="submit" class="update-role-button">Remove Selected Roles</button>
        </form>
        <div v-if="removeRoleMessage" class="form-message" :class="{ success: removeRoleSuccess, error: !removeRoleSuccess }">
          {{ removeRoleMessage }}
        </div>
      </div>
      <div class="data-widget create-role-widget">
        <h3>Create New Role</h3>
        <div class="form-group">
          <label>Live Preview</label>
          <span
            class="role-badge"
            :class="newRole.name.toLowerCase()"
            :style="{ background: newRole.badge_color || '#888' }"
          >
            <i v-if="newRole.badge_icon" :class="newRole.badge_icon"></i>
            {{ newRole.name || 'Role Name' }}
          </span>
        </div>
        <form @submit.prevent="$emit('createRole')" class="create-role-form">
          <div class="form-group">
            <label for="role-name">Role Name</label>
            <input 
              id="role-name" 
              :value="newRole.name" 
              @input="updateNewRole('name', $event.target.value)" 
              required 
              placeholder="Role name (e.g. Producer)" />
          </div>
          <div class="form-group">
            <label for="role-badge-icon">Badge Icon (Font Awesome class)</label>
            <input 
              id="role-badge-icon" 
              :value="newRole.badge_icon" 
              @input="updateNewRole('badge_icon', $event.target.value)" 
              placeholder="e.g. fas fa-microphone" />
          </div>
          <div class="form-group">
            <label for="role-badge-color">Badge Color</label>
<input
  id="role-badge-color"
  :value="newRole.badge_color || '#888888'"
  @input="updateNewRole('badge_color', $event.target.value)"
  type="color"
  style="width: 40px; height: 40px; padding: 0; border: none; vertical-align: middle;"
/>
            <input
              :value="newRole.badge_color"
              @input="updateNewRole('badge_color', $event.target.value)"
              placeholder="#43b581 or gradient"
              style="margin-left: 0.5rem; width: 120px;"
            />
          </div>
          <button type="submit" class="create-role-button">Create Role</button>
        </form>
        <div v-if="createRoleMessage" class="form-message" :class="{ success: createRoleSuccess, error: !createRoleSuccess }">
          {{ createRoleMessage }}
        </div>
        <div v-if="availableRoles.length" class="roles-list">
          <h4>Existing Roles</h4>
          <div class="roles-list-flex">
            <div v-for="role in availableRoles" :key="role.id" class="role-list-item">
              <span
                class="role-badge"
                :style="{ backgroundColor: role.badge_color || '#888' }"
              >
                <i v-if="role.badge_icon" :class="role.badge_icon"></i>
                {{ role.name }}
              </span>
              <button class="delete-role-button" @click="$emit('deleteRole', role.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
      <div class="data-widget">
        <h3>Manage User Achievements</h3>
        <form @submit.prevent="deleteUserAchievement">
          <div class="form-group">
            <label for="user-select-achv">Select User</label>
            <select
              id="user-select-achv"
              v-model="achvUserId"
              @change="fetchUserAchievements"
            >
              <option value="" disabled>Select a user</option>
              <option v-for="user in usersList" :key="user.id" :value="user.id">
                {{ user.username ? user.username + ', ' + user.email : user.email }}
              </option>
            </select>
          </div>
          <div v-if="userAchievements.length > 0">
            <label>Achievements:</label>
            <div class="checkbox-group-vertical">
              <label
                v-for="achv in userAchievements"
                :key="achv.achievement_id"
                class="custom-checkbox"
              >
                <input
                  type="checkbox"
                  :value="achv.achievement_id"
                  v-model="selectedAchievements"
                />
                {{ achv.name || achv.title }} <span v-if="achv.unlocked_at"> (Unlocked: {{ achv.unlocked_at.slice(0, 10) }})</span>
              </label>
            </div>
          </div>
          <div v-else-if="achvUserId">
            <p>No achievements unlocked yet.</p>
          </div>
          <button type="submit" class="update-role-button" :disabled="selectedAchievements.length === 0">
            Remove Selected Achievements
          </button>
        </form>
        <div v-if="achvRemoveMessage" class="form-message" :class="{ success: achvRemoveSuccess, error: !achvRemoveSuccess }">
          {{ achvRemoveMessage }}
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: [
    'userRoles',
    'usersList',
    'userRoleUpdate',
    'availableRoles',
    'updateUserMessage',
    'updateUserSuccess',
    'selectedUserRoles',
    'userRoleRemove',
    'selectedUserRolesToRemove',
    'rolesToRemove',
    'removeRoleMessage',
    'removeRoleSuccess',
    'newRole',
    'createRoleMessage',
    'createRoleSuccess'
  ],
  emits: [
    'updateUserRole',
    'fetchUserRolesToRemove',
    'removeSelectedRoles',
    'createRole',
    'deleteRole',
    'update:userRoleUpdate',
    'update:userRoleRemove',
    'update:rolesToRemove',
    'update:newRole'
  ],
  data() {
    return {
      // --- Achievements section state ---
      achvUserId: '',                 // Selected user for achievements
      userAchievements: [],           // Achievements fetched for user
      selectedAchievements: [],       // Which achievements are checked for removal
      achvRemoveMessage: '',          // Feedback message
      achvRemoveSuccess: false        // Success status
    }
  },
  methods: {
    updateUserRoleUpdate(field, value) {
      const updated = { ...this.userRoleUpdate, [field]: value };
      this.$emit('update:userRoleUpdate', updated);
    },
    onUserRoleRemoveChange(value) {
      const updated = { ...this.userRoleRemove, selectedUser: value };
      this.$emit('update:userRoleRemove', updated);
      this.$emit('fetchUserRolesToRemove');
    },
    toggleRoleToRemove(roleId) {
      let updatedRoles;
      if (this.rolesToRemove.includes(roleId)) {
        updatedRoles = this.rolesToRemove.filter(id => id !== roleId);
      } else {
        updatedRoles = [...this.rolesToRemove, roleId];
      }
      this.$emit('update:rolesToRemove', updatedRoles);
    },
    updateNewRole(field, value) {
      const updated = { ...this.newRole, [field]: value };
      this.$emit('update:newRole', updated);
    },
    // --- Achievements Management ---
    async fetchUserAchievements() {
      if (!this.achvUserId) {
        this.userAchievements = [];
        return;
      }
      try {
        const apiBase = import.meta.env.VITE_API_URL; // should be http://localhost:5000/api
        const response = await fetch(`${apiBase}/user/${this.achvUserId}/achievements`, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token')
          }
        });
        if (!response.ok) {
          const errorText = await response.text();
          console.error('Error response:', errorText);
          throw new Error('Failed to fetch achievements');
        }
        const data = await response.json();
        this.userAchievements = data;
        this.selectedAchievements = [];
        this.achvRemoveMessage = '';
        this.achvRemoveSuccess = false;
      } catch (e) {
        this.userAchievements = [];
        this.achvRemoveMessage = 'Failed to fetch achievements.';
        this.achvRemoveSuccess = false;
        console.error('Error fetching achievements:', e);
      }
    },
    async deleteUserAchievement() {
      if (this.selectedAchievements.length === 0) {
        this.achvRemoveMessage = "No achievements selected.";
        this.achvRemoveSuccess = false;
        return;
      }
      try {
        // Remove one at a time (for simplicity)
        for (const achvId of this.selectedAchievements) {
          const apiBase = import.meta.env.VITE_API_URL; // should be http://localhost:5000/api
          await fetch(`${apiBase}/admin/delete-user-achievement`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('access_token')
            },
            body: JSON.stringify({
              user_id: this.achvUserId,
              achievement_id: achvId
            })
          });
        }
        this.achvRemoveMessage = "Selected achievements removed!";
        this.achvRemoveSuccess = true;
        this.selectedAchievements = [];
        await this.fetchUserAchievements(); // Refresh the list
      } catch (e) {
        this.achvRemoveMessage = "Failed to remove achievements.";
        this.achvRemoveSuccess = false;
      }
    }
  }
}
</script>


<style scoped>
/* Admin widgets row: flexbox for horizontal layout */
.admin-widgets-row {
  display: flex;
  flex-wrap: wrap; /* Allows wrapping on smaller screens */
  gap: 2rem;       /* Space between widgets */
  justify-content: flex-start;
  align-items: flex-start;
}

/* Each widget: flexible width, min and max for responsiveness */
.data-widget {
  flex: 1 1 320px;      /* Grow, shrink, min width */
  max-width: 400px;     /* Prevents widgets from getting too wide */
  min-width: 280px;     /* Prevents widgets from getting too narrow */
  margin-bottom: 2rem;  /* Space below for wrapping */
}

/* Responsive: stack on mobile */
@media (max-width: 900px) {
  .admin-widgets-row {
    flex-direction: column;
    gap: 1.5rem;
  }
  .data-widget {
    max-width: 100%;
    min-width: 0;
  }
}
</style>
